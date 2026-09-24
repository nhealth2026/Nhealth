"""
Nhealth - Database Layer
Supports Neon Serverless PostgreSQL with seamless JSON Flat-file fallback.
"""

import os
import json
import time
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor, Json
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Data directory for JSON fallback
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
CONTACTS_FILE = os.path.join(DATA_DIR, 'contacts.json')

# Neon PostgreSQL Connection URL from env
DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('NEON_DATABASE_URL') or os.environ.get('POSTGRES_URL')

# Fix postgres:// URL prefix if provided by cloud providers (SQLAlchemy / psycopg2 compatibility)
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Thread-safe Connection Pool for Neon
_pg_pool = None
_db_connected = False

def init_db():
    """Initialize PostgreSQL tables if DATABASE_URL is configured."""
    global _pg_pool, _db_connected
    if not DATABASE_URL:
        print("[DB] No DATABASE_URL found. Using local JSON file storage (data/).")
        _init_json_files()
        return False

    try:
        # Create threaded connection pool
        _pg_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=DATABASE_URL,
            sslmode='require'
        )
        
        # Test connection & create tables
        conn = _pg_pool.getconn()
        with conn.cursor() as cur:
            # Users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(64) PRIMARY KEY,
                    email VARCHAR(255) UNIQUE,
                    phone VARCHAR(32) UNIQUE,
                    role VARCHAR(32) NOT NULL DEFAULT 'patient',
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(255),
                    lab_name VARCHAR(255),
                    owner_name VARCHAR(255),
                    address TEXT,
                    city VARCHAR(100),
                    state VARCHAR(100),
                    pincode VARCHAR(20),
                    reg_number VARCHAR(100),
                    gst_number VARCHAR(100),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    extra_data JSONB DEFAULT '{}'::jsonb
                );
            """)

            # Bookings table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id SERIAL PRIMARY KEY,
                    booking_id VARCHAR(64) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(32) NOT NULL,
                    email VARCHAR(255),
                    service VARCHAR(255) NOT NULL,
                    city VARCHAR(100),
                    address TEXT,
                    preferred_date VARCHAR(64),
                    time_slot VARCHAR(100),
                    notes TEXT,
                    status VARCHAR(50) DEFAULT 'Confirmed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    extra_data JSONB DEFAULT '{}'::jsonb
                );
            """)

            # Contacts table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id VARCHAR(64) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    phone VARCHAR(32) NOT NULL,
                    subject VARCHAR(255),
                    message TEXT NOT NULL,
                    status VARCHAR(50) DEFAULT 'new',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
        _pg_pool.putconn(conn)
        _db_connected = True
        print("[DB] Successfully connected to Neon PostgreSQL and verified schemas.")
        return True
    except Exception as e:
        print(f"[DB Warning] Could not connect to Neon PostgreSQL: {e}")
        print("[DB] Falling back to local JSON files.")
        _db_connected = False
        _init_json_files()
        return False

def _init_json_files():
    for fpath in [BOOKINGS_FILE, USERS_FILE, CONTACTS_FILE]:
        if not os.path.exists(fpath):
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump([], f)

def get_connection():
    if _db_connected and _pg_pool:
        return _pg_pool.getconn()
    return None

def release_connection(conn):
    if _db_connected and _pg_pool and conn:
        try:
            _pg_pool.putconn(conn)
        except Exception:
            pass

# ==================== USER OPERATIONS ====================

def get_all_users():
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users ORDER BY created_at DESC;")
                rows = cur.fetchall()
                results = []
                for row in rows:
                    u = dict(row)
                    # Merge extra_data into top-level dictionary
                    if u.get('extra_data') and isinstance(u['extra_data'], dict):
                        for k, v in u['extra_data'].items():
                            if k not in u or u[k] is None:
                                u[k] = v
                    results.append(u)
                return results
        except Exception as e:
            print(f"[DB Error get_all_users]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

from datetime import datetime, date

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return str(obj)

def safe_json(d):
    return Json(d, dumps=lambda o: json.dumps(o, default=json_serial))

def save_user(user_data):
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                # Separate standard columns from extra metadata
                known_keys = {
                    'id', 'email', 'phone', 'role', 'password', 'name',
                    'lab_name', 'owner_name', 'address', 'city', 'state',
                    'pincode', 'reg_number', 'gst_number', 'is_active', 'created_at'
                }
                extra = {k: v for k, v in user_data.items() if k not in known_keys}

                email_val = user_data.get('email') or None
                phone_val = user_data.get('phone') or None

                cur.execute("""
                    INSERT INTO users (
                        id, email, phone, role, password, name,
                        lab_name, owner_name, address, city, state,
                        pincode, reg_number, gst_number, is_active, extra_data
                    ) VALUES (
                        %(id)s, %(email)s, %(phone)s, %(role)s, %(password)s, %(name)s,
                        %(lab_name)s, %(owner_name)s, %(address)s, %(city)s, %(state)s,
                        %(pincode)s, %(reg_number)s, %(gst_number)s, %(is_active)s, %(extra_data)s
                    ) ON CONFLICT (id) DO UPDATE SET
                        email = EXCLUDED.email,
                        phone = EXCLUDED.phone,
                        name = EXCLUDED.name,
                        address = EXCLUDED.address,
                        city = EXCLUDED.city,
                        extra_data = EXCLUDED.extra_data;
                """, {
                    'id': user_data.get('id'),
                    'email': email_val,
                    'phone': phone_val,
                    'role': user_data.get('role', 'patient'),
                    'password': user_data.get('password', ''),
                    'name': user_data.get('name') or user_data.get('lab_name'),
                    'lab_name': user_data.get('lab_name'),
                    'owner_name': user_data.get('owner_name'),
                    'address': user_data.get('address'),
                    'city': user_data.get('city'),
                    'state': user_data.get('state'),
                    'pincode': user_data.get('pincode'),
                    'reg_number': user_data.get('reg_number'),
                    'gst_number': user_data.get('gst_number'),
                    'is_active': user_data.get('is_active', True),
                    'extra_data': safe_json(extra)
                })
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"[DB Error save_user]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    users = get_all_users()
    users.append(user_data)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, default=json_serial)
    return True

def update_user(user_id, updated_fields):
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                known_keys = {
                    'email', 'phone', 'name', 'lab_name', 'owner_name',
                    'address', 'city', 'state', 'pincode', 'reg_number', 'gst_number'
                }
                set_clauses = []
                values = {'id': user_id}

                for k, v in updated_fields.items():
                    if k in known_keys:
                        set_clauses.append(f"{k} = %({k})s")
                        values[k] = v
                
                # Check for extra data fields
                extra_updates = {k: v for k, v in updated_fields.items() if k not in known_keys and k not in ('id', 'password')}
                if extra_updates:
                    set_clauses.append("extra_data = COALESCE(extra_data, '{}'::jsonb) || %(extra_json)s::jsonb")
                    values['extra_json'] = json.dumps(extra_updates)

                if set_clauses:
                    query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %(id)s;"
                    cur.execute(query, values)
                    conn.commit()
                    return True
        except Exception as e:
            conn.rollback()
            print(f"[DB Error update_user]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    users = get_all_users()
    updated = False
    for u in users:
        if u.get('id') == user_id:
            for k, v in updated_fields.items():
                if k != 'id' and k != 'password':
                    u[k] = v
            updated = True
            break
    if updated:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)
    return updated

# ==================== BOOKINGS OPERATIONS ====================

def get_all_bookings():
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM bookings ORDER BY created_at DESC;")
                rows = cur.fetchall()
                results = []
                for row in rows:
                    b = dict(row)
                    if b.get('extra_data') and isinstance(b['extra_data'], dict):
                        for k, v in b['extra_data'].items():
                            if k not in b:
                                b[k] = v
                    results.append(b)
                return results
        except Exception as e:
            print(f"[DB Error get_all_bookings]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    try:
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_booking(booking_record):
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                known_keys = {
                    'booking_id', 'name', 'phone', 'email', 'service',
                    'city', 'address', 'preferred_date', 'time_slot', 'notes', 'status'
                }
                extra = {k: v for k, v in booking_record.items() if k not in known_keys}

                cur.execute("""
                    INSERT INTO bookings (
                        booking_id, name, phone, email, service,
                        city, address, preferred_date, time_slot, notes, status, extra_data
                    ) VALUES (
                        %(booking_id)s, %(name)s, %(phone)s, %(email)s, %(service)s,
                        %(city)s, %(address)s, %(preferred_date)s, %(time_slot)s, %(notes)s, %(status)s, %(extra_data)s
                    );
                """, {
                    'booking_id': booking_record.get('booking_id'),
                    'name': booking_record.get('name'),
                    'phone': booking_record.get('phone'),
                    'email': booking_record.get('email', ''),
                    'service': booking_record.get('service'),
                    'city': booking_record.get('city', ''),
                    'address': booking_record.get('address', ''),
                    'preferred_date': booking_record.get('preferred_date', ''),
                    'time_slot': booking_record.get('time_slot', ''),
                    'notes': booking_record.get('notes', ''),
                    'status': booking_record.get('status', 'Confirmed'),
                    'extra_data': Json(extra)
                })
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"[DB Error save_booking]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    try:
        with open(BOOKINGS_FILE, 'r+', encoding='utf-8') as f:
            records = json.load(f)
            records.append(booking_record)
            f.seek(0)
            json.dump(records, f, indent=2)
    except Exception:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump([booking_record], f, indent=2)
    return True

# ==================== CONTACTS OPERATIONS ====================

def get_all_contacts():
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM contacts ORDER BY created_at DESC;")
                return [dict(r) for r in cur.fetchall()]
        except Exception as e:
            print(f"[DB Error get_all_contacts]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_contact(contact_entry):
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO contacts (id, name, email, phone, subject, message, status)
                    VALUES (%(id)s, %(name)s, %(email)s, %(phone)s, %(subject)s, %(message)s, %(status)s);
                """, contact_entry)
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"[DB Error save_contact]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    try:
        contacts = get_all_contacts()
        contacts.append(contact_entry)
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=2)
    except Exception as e:
        print(f"[Contact Save Error]: {e}")
    return True

# Initialize on module load
init_db()

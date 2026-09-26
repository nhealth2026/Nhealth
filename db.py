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
            sslmode='require',
            connect_timeout=3
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

            # Rider Real-Time Trips table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rider_trips (
                    id SERIAL PRIMARY KEY,
                    trip_id VARCHAR(64) UNIQUE NOT NULL,
                    rider_id VARCHAR(64),
                    rider_name VARCHAR(255),
                    rider_phone VARCHAR(32),
                    rider_vehicle VARCHAR(255),
                    patient_name VARCHAR(255) NOT NULL,
                    patient_phone VARCHAR(32) NOT NULL,
                    task_type VARCHAR(100) NOT NULL,
                    pickup_address TEXT NOT NULL,
                    pickup_lat FLOAT DEFAULT 16.5062,
                    pickup_lng FLOAT DEFAULT 80.6480,
                    drop_address TEXT NOT NULL,
                    drop_lat FLOAT DEFAULT 16.5150,
                    drop_lng FLOAT DEFAULT 80.6350,
                    rider_lat FLOAT DEFAULT 16.5020,
                    rider_lng FLOAT DEFAULT 80.6430,
                    rider_heading FLOAT DEFAULT 0,
                    fare_amount INT DEFAULT 120,
                    distance_km FLOAT DEFAULT 2.5,
                    start_otp VARCHAR(10) NOT NULL DEFAULT '4829',
                    status VARCHAR(50) DEFAULT 'searching',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    extra_data JSONB DEFAULT '{}'::jsonb
                );
            """)
            conn.commit()
        _pg_pool.putconn(conn)
        _db_connected = True
        print("[DB] Successfully connected to Neon PostgreSQL and verified schemas.")
        _seed_demo_accounts()
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

from datetime import datetime, date

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return str(obj)

def safe_json(d):
    return Json(d, dumps=lambda o: json.dumps(o, default=json_serial))

def _clean_record(rec):
    """Recursively convert datetime/date objects to ISO format strings."""
    if not isinstance(rec, dict):
        return rec
    cleaned = {}
    for k, v in rec.items():
        if isinstance(v, (datetime, date)):
            cleaned[k] = v.isoformat()
        elif isinstance(v, dict):
            cleaned[k] = _clean_record(v)
        elif isinstance(v, list):
            cleaned[k] = [
                _clean_record(item) if isinstance(item, dict)
                else (item.isoformat() if isinstance(item, (datetime, date)) else item)
                for item in v
            ]
        else:
            cleaned[k] = v
    return cleaned

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
                    results.append(_clean_record(u))
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
                    results.append(_clean_record(b))
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
                    'extra_data': safe_json(extra)
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
            json.dump(records, f, indent=2, default=json_serial)
    except Exception:
        with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump([booking_record], f, indent=2, default=json_serial)
    return True

# ==================== CONTACTS OPERATIONS ====================

def get_all_contacts():
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM contacts ORDER BY created_at DESC;")
                return [_clean_record(dict(r)) for r in cur.fetchall()]
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

# ==================== RIDER & TRIPS OPERATIONS ====================

TRIPS_FILE = os.path.join(DATA_DIR, 'trips.json')
if not os.path.exists(TRIPS_FILE):
    with open(TRIPS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def _seed_demo_accounts():
    """Ensure Demo Rider, Patient, and Doctor exist in the database."""
    demo_rider = {
        'id': 'USR-RIDER-001',
        'email': 'rider@nhealth.in',
        'phone': '9876543222',
        'role': 'rider',
        'password': 'password123',
        'name': 'Ravi Varma',
        'city': 'Vijayawada',
        'state': 'Andhra Pradesh',
        'pincode': '520010',
        'reg_number': 'AP-DL-2024-8849',
        'is_active': True,
        'vehicle_type': 'Motorcycle (Hero Splendor+)',
        'vehicle_number': 'AP 16 CK 4589',
        'is_online': True,
        'rating': '4.9',
        'total_rides': 142,
        'current_lat': 16.5020,
        'current_lng': 80.6430,
        'heading': 45
    }
    try:
        users = get_all_users()
        has_rider = any(u.get('email') == 'rider@nhealth.in' or str(u.get('phone')) == '9876543222' for u in users)
        if not has_rider:
            save_user(demo_rider)
            print("[DB Seed] Seeded demo rider (rider@nhealth.in).")
    except Exception as e:
        print(f"[DB Seed Error]: {e}")

def update_rider_duty_status(rider_id, is_online):
    """Toggle online/offline duty status for rider."""
    return update_user(rider_id, {'is_online': bool(is_online)})

def update_rider_location(rider_id, lat, lng, heading=0, active_trip_id=None):
    """Update current GPS coordinates and heading for rider."""
    update_data = {
        'current_lat': float(lat),
        'current_lng': float(lng),
        'heading': float(heading),
        'last_location_time': datetime.now().isoformat()
    }
    update_user(rider_id, update_data)

    if active_trip_id:
        if _db_connected:
            conn = get_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE rider_trips
                        SET rider_lat = %s, rider_lng = %s, rider_heading = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE trip_id = %s;
                    """, (float(lat), float(lng), float(heading), active_trip_id))
                    conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"[DB Error update_trip_location]: {e}")
            finally:
                release_connection(conn)

    return True

def create_rider_trip(trip_data):
    """Create a new health support ride / delivery task."""
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO rider_trips (
                        trip_id, rider_id, rider_name, rider_phone, rider_vehicle,
                        patient_name, patient_phone, task_type,
                        pickup_address, pickup_lat, pickup_lng,
                        drop_address, drop_lat, drop_lng,
                        rider_lat, rider_lng, rider_heading,
                        fare_amount, distance_km, start_otp, status, extra_data
                    ) VALUES (
                        %(trip_id)s, %(rider_id)s, %(rider_name)s, %(rider_phone)s, %(rider_vehicle)s,
                        %(patient_name)s, %(patient_phone)s, %(task_type)s,
                        %(pickup_address)s, %(pickup_lat)s, %(pickup_lng)s,
                        %(drop_address)s, %(drop_lat)s, %(drop_lng)s,
                        %(rider_lat)s, %(rider_lng)s, %(rider_heading)s,
                        %(fare_amount)s, %(distance_km)s, %(start_otp)s, %(status)s, %(extra_data)s
                    );
                """, {
                    'trip_id': trip_data.get('trip_id'),
                    'rider_id': trip_data.get('rider_id'),
                    'rider_name': trip_data.get('rider_name'),
                    'rider_phone': trip_data.get('rider_phone'),
                    'rider_vehicle': trip_data.get('rider_vehicle'),
                    'patient_name': trip_data.get('patient_name'),
                    'patient_phone': trip_data.get('patient_phone'),
                    'task_type': trip_data.get('task_type', 'Patient OPD Accompaniment'),
                    'pickup_address': trip_data.get('pickup_address', 'Benz Circle, Vijayawada'),
                    'pickup_lat': trip_data.get('pickup_lat', 16.5062),
                    'pickup_lng': trip_data.get('pickup_lng', 80.6480),
                    'drop_address': trip_data.get('drop_address', 'Ramesh Hospitals, Vijayawada'),
                    'drop_lat': trip_data.get('drop_lat', 16.5150),
                    'drop_lng': trip_data.get('drop_lng', 80.6350),
                    'rider_lat': trip_data.get('rider_lat', 16.5020),
                    'rider_lng': trip_data.get('rider_lng', 80.6430),
                    'rider_heading': trip_data.get('rider_heading', 0),
                    'fare_amount': trip_data.get('fare_amount', 120),
                    'distance_km': trip_data.get('distance_km', 2.5),
                    'start_otp': trip_data.get('start_otp', '4829'),
                    'status': trip_data.get('status', 'searching'),
                    'extra_data': safe_json(trip_data.get('extra_data', {}))
                })
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"[DB Error create_rider_trip]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    try:
        with open(TRIPS_FILE, 'r+', encoding='utf-8') as f:
            trips = json.load(f)
            trips.append(trip_data)
            f.seek(0)
            json.dump(trips, f, indent=2, default=json_serial)
    except Exception:
        with open(TRIPS_FILE, 'w', encoding='utf-8') as f:
            json.dump([trip_data], f, indent=2, default=json_serial)
    return True

def generate_next_invoice_number(prefix="NH-INV"):
    """Generate an automatic, sequential invoice number for today: NH-INV-YYYYMMDD-XXXX."""
    today_str = datetime.now().strftime("%Y%m%d")
    search_prefix = f"{prefix}-{today_str}-"
    next_seq = 1

    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT extra_data->>'invoice_number'
                    FROM rider_trips
                    WHERE extra_data->>'invoice_number' LIKE %s;
                """, (search_prefix + '%',))
                rows = cur.fetchall()
                numbers = []
                for r in rows:
                    inv = r[0] if r else None
                    if inv and inv.startswith(search_prefix):
                        try:
                            seq_part = int(inv.replace(search_prefix, ''))
                            numbers.append(seq_part)
                        except (ValueError, TypeError):
                            pass
                if numbers:
                    next_seq = max(numbers) + 1
        except Exception as e:
            print(f"[Invoice Number Gen Error]: {e}")
        finally:
            release_connection(conn)
    else:
        try:
            if os.path.exists(TRIPS_FILE):
                with open(TRIPS_FILE, 'r', encoding='utf-8') as f:
                    trips = json.load(f)
                    numbers = []
                    for t in trips:
                        extra = t.get('extra_data') or {}
                        if isinstance(extra, str):
                            try:
                                extra = json.loads(extra)
                            except Exception:
                                extra = {}
                        inv = extra.get('invoice_number') or t.get('invoice_number')
                        if inv and inv.startswith(search_prefix):
                            try:
                                seq_part = int(inv.replace(search_prefix, ''))
                                numbers.append(seq_part)
                            except (ValueError, TypeError):
                                pass
                    if numbers:
                        next_seq = max(numbers) + 1
        except Exception:
            pass

    return f"{search_prefix}{next_seq:04d}"

def get_trip_by_id(trip_id):
    """Retrieve trip by trip_id."""
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM rider_trips WHERE trip_id = %s;", (trip_id,))
                row = cur.fetchone()
                if row:
                    return _clean_record(dict(row))
        except Exception as e:
            print(f"[DB Error get_trip_by_id]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    try:
        with open(TRIPS_FILE, 'r', encoding='utf-8') as f:
            trips = json.load(f)
            for t in trips:
                if t.get('trip_id') == trip_id:
                    return _clean_record(t)
    except Exception:
        pass
    return None

def get_all_trips():
    """Retrieve all rider trips."""
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM rider_trips ORDER BY created_at DESC;")
                return [_clean_record(dict(r)) for r in cur.fetchall()]
        except Exception as e:
            print(f"[DB Error get_all_trips]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    try:
        with open(TRIPS_FILE, 'r', encoding='utf-8') as f:
            return [_clean_record(t) for t in json.load(f)]
    except Exception:
        return []

def get_available_tasks_for_riders():
    """Fetch all pending / unassigned tasks for riders to accept."""
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM rider_trips
                    WHERE status IN ('searching', 'pending')
                    ORDER BY created_at DESC LIMIT 10;
                """)
                return [_clean_record(dict(r)) for r in cur.fetchall()]
        except Exception as e:
            print(f"[DB Error get_available_tasks]: {e}")
        finally:
            release_connection(conn)

    trips = get_all_trips()
    return [t for t in trips if t.get('status') in ('searching', 'pending')]

def accept_trip_by_rider(trip_id, rider_id, rider_name, rider_phone, rider_vehicle, rider_lat=None, rider_lng=None):
    """Rider accepts an incoming task. Optionally seeds rider_lat/lng from their current GPS position."""
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                if rider_lat is not None and rider_lng is not None:
                    cur.execute("""
                        UPDATE rider_trips
                        SET rider_id = %s, rider_name = %s, rider_phone = %s, rider_vehicle = %s,
                            rider_lat = %s, rider_lng = %s,
                            status = 'accepted', updated_at = CURRENT_TIMESTAMP
                        WHERE trip_id = %s AND status IN ('searching', 'pending');
                    """, (rider_id, rider_name, rider_phone, rider_vehicle, float(rider_lat), float(rider_lng), trip_id))
                else:
                    cur.execute("""
                        UPDATE rider_trips
                        SET rider_id = %s, rider_name = %s, rider_phone = %s, rider_vehicle = %s,
                            status = 'accepted', updated_at = CURRENT_TIMESTAMP
                        WHERE trip_id = %s AND status IN ('searching', 'pending');
                    """, (rider_id, rider_name, rider_phone, rider_vehicle, trip_id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"[DB Error accept_trip]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    trips = get_all_trips()
    for t in trips:
        if t.get('trip_id') == trip_id:
            t['rider_id'] = rider_id
            t['rider_name'] = rider_name
            t['rider_phone'] = rider_phone
            t['rider_vehicle'] = rider_vehicle
            t['status'] = 'accepted'
            break
    with open(TRIPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(trips, f, indent=2, default=json_serial)
    return True

def update_trip_status(trip_id, status):
    """Update trip status (arrived, in_transit, completed, cancelled)."""
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE rider_trips
                    SET status = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE trip_id = %s;
                """, (status, trip_id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            print(f"[DB Error update_trip_status]: {e}")
        finally:
            release_connection(conn)

    # JSON Fallback
    trips = get_all_trips()
    for t in trips:
        if t.get('trip_id') == trip_id:
            t['status'] = status
            break
    with open(TRIPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(trips, f, indent=2, default=json_serial)
    return True

def verify_trip_otp(trip_id, otp):
    """Verify 4-digit start OTP provided by patient."""
    trip = get_trip_by_id(trip_id)
    if not trip:
        return False, "Trip not found"
    if str(trip.get('start_otp')).strip() == str(otp).strip():
        update_trip_status(trip_id, 'in_transit')
        return True, "OTP verified successfully. Journey started!"
    return False, "Invalid OTP. Please ask the patient for their 4-digit OTP."

def get_rider_trip_history(rider_id):
    """Fetch completed, ended, or cancelled trips for a rider history view."""
    if _db_connected:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM rider_trips
                    WHERE rider_id = %s AND status IN ('completed', 'ended', 'cancelled')
                    ORDER BY updated_at DESC, created_at DESC LIMIT 50;
                """, (rider_id,))
                return [_clean_record(dict(r)) for r in cur.fetchall()]
        except Exception as e:
            print(f"[DB Error get_rider_trip_history]: {e}")
        finally:
            release_connection(conn)

    trips = get_all_trips()
    history = [t for t in trips if t.get('rider_id') == rider_id and t.get('status') in ('completed', 'ended', 'cancelled')]
    history.sort(key=lambda x: x.get('updated_at') or x.get('created_at') or '', reverse=True)
    return history

# Initialize on module load
init_db()


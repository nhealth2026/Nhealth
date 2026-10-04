import os
import json
import time
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor, Json
from dotenv import load_dotenv
from datetime import datetime, date

# Load environment variables from .env if present
load_dotenv()

# Data directory for JSON fallback
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
# Since original was __file__ which was at d:/nhealth final/db.py, 
# but now we are at d:/nhealth final/backend/models/base.py
# So we need to go up two directories for 'data' at the root, or keep it in models/data.
# The original code: os.path.join(os.path.dirname(__file__), 'data') -> d:/nhealth final/data
# In new file: os.path.dirname(__file__) is backend/models
# To match original behaviour assuming db.py was in root:
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
CONTACTS_FILE = os.path.join(DATA_DIR, 'contacts.json')
TRIPS_FILE = os.path.join(DATA_DIR, 'trips.json')
if not os.path.exists(TRIPS_FILE):
    with open(TRIPS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

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
        try:
            from backend.seeds.demo_accounts import _seed_demo_accounts
            _seed_demo_accounts()
        except Exception as err:
            print(f"[DB Seed Warning]: {err}")
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
        from backend.seeds.demo_accounts import _seed_demo_accounts
        _seed_demo_accounts()
        return True
    except Exception as e:
        print(f"[DB Warning] Could not connect to Neon PostgreSQL: {e}")
        print("[DB] Falling back to local JSON files.")
        _db_connected = False
        _init_json_files()
        try:
            from backend.seeds.demo_accounts import _seed_demo_accounts
            _seed_demo_accounts()
        except Exception:
            pass
        return False

def _init_json_files():
    for fpath in [BOOKINGS_FILE, USERS_FILE, CONTACTS_FILE]:
        if not os.path.exists(fpath):
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump([], f)

def _safe_rollback(conn):
    if conn:
        try:
            conn.rollback()
        except Exception:
            pass

def get_connection():
    if _db_connected and _pg_pool:
        try:
            conn = _pg_pool.getconn()
            if conn and getattr(conn, 'closed', 0) != 0:
                _pg_pool.putconn(conn, close=True)
                conn = _pg_pool.getconn()
            return conn
        except Exception as e:
            print(f"[DB Pool Warning]: {e}")
            return None
    return None

def release_connection(conn, is_broken=False):
    if _db_connected and _pg_pool and conn:
        try:
            if is_broken or getattr(conn, 'closed', 0) != 0:
                _pg_pool.putconn(conn, close=True)
            else:
                _pg_pool.putconn(conn)
        except Exception:
            pass

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

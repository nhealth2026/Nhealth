import os
import json
from datetime import datetime
from psycopg2.extras import RealDictCursor

from .base import (
    get_connection, release_connection, _safe_rollback, _clean_record,
    safe_json, json_serial, TRIPS_FILE, _db_connected
)

from .users import update_user, get_all_users

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
            _safe_rollback(conn)
            print(f"[DB Error create_rider_trip]: {e}")
            release_connection(conn, is_broken=True)
            conn = None
        finally:
            if conn:
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
            _safe_rollback(conn)
            print(f"[DB Error accept_trip]: {e}")
            release_connection(conn, is_broken=True)
            conn = None
        finally:
            if conn:
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
            _safe_rollback(conn)
            print(f"[DB Error update_trip_status]: {e}")
            release_connection(conn, is_broken=True)
            conn = None
        finally:
            if conn:
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

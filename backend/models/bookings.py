import json
from psycopg2.extras import RealDictCursor

from .base import (
    get_connection, release_connection, _clean_record, safe_json,
    json_serial, BOOKINGS_FILE, _db_connected
)

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

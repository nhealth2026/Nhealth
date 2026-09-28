import os
import json
from psycopg2.extras import RealDictCursor

from .base import (
    get_connection, release_connection, _safe_rollback, _clean_record,
    safe_json, json_serial, USERS_FILE, _db_connected
)

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
            _safe_rollback(conn)
            print(f"[DB Error save_user]: {e}")
            release_connection(conn, is_broken=True)
            conn = None
        finally:
            if conn:
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
            _safe_rollback(conn)
            print(f"[DB Error update_user]: {e}")
            release_connection(conn, is_broken=True)
            conn = None
        finally:
            if conn:
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

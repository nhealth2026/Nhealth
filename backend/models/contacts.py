import json
from psycopg2.extras import RealDictCursor

from .base import (
    get_connection, release_connection, _clean_record,
    CONTACTS_FILE, _db_connected
)

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

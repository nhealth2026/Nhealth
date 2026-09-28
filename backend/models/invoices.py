import os
import json
from datetime import datetime

from .base import (
    get_connection, release_connection, _db_connected, TRIPS_FILE
)

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

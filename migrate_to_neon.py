"""
Nhealth - Data Migration Script: JSON to Neon PostgreSQL
Migrates all existing records from data/*.json into Neon PostgreSQL tables.
"""

import os
import json
import sys
from dotenv import load_dotenv
import db

load_dotenv()

def migrate():
    print("=" * 60)
    print(">> Nhealth - Neon PostgreSQL Data Migration")
    print("=" * 60)

    if not db.DATABASE_URL:
        print("[ERROR] No DATABASE_URL found in .env or environment.")
        return

    print("Connecting to Neon PostgreSQL...")
    connected = db.init_db()
    if not connected or not db._db_connected:
        print("[ERROR] Failed to connect to Neon PostgreSQL. Check your DATABASE_URL.")
        return

    # 1. Migrate Users
    users_path = os.path.join(db.DATA_DIR, 'users.json')
    if os.path.exists(users_path):
        try:
            with open(users_path, 'r', encoding='utf-8') as f:
                users = json.load(f)
            print(f"\n[Users] Found {len(users)} user record(s) in users.json.")
            migrated_users = 0
            for u in users:
                if db.save_user(u):
                    migrated_users += 1
            print(f"[Users] Successfully migrated {migrated_users}/{len(users)} users to Neon PostgreSQL.")
        except Exception as e:
            print(f"[Users Error]: {e}")

    # 2. Migrate Bookings
    bookings_path = os.path.join(db.DATA_DIR, 'bookings.json')
    if os.path.exists(bookings_path):
        try:
            with open(bookings_path, 'r', encoding='utf-8') as f:
                bookings = json.load(f)
            print(f"\n[Bookings] Found {len(bookings)} booking record(s) in bookings.json.")
            migrated_bookings = 0
            for b in bookings:
                if db.save_booking(b):
                    migrated_bookings += 1
            print(f"[Bookings] Successfully migrated {migrated_bookings}/{len(bookings)} bookings to Neon PostgreSQL.")
        except Exception as e:
            print(f"[Bookings Error]: {e}")

    # 3. Migrate Contacts
    contacts_path = os.path.join(db.DATA_DIR, 'contacts.json')
    if os.path.exists(contacts_path):
        try:
            with open(contacts_path, 'r', encoding='utf-8') as f:
                contacts = json.load(f)
            print(f"\n[Contacts] Found {len(contacts)} contact inquiry record(s) in contacts.json.")
            migrated_contacts = 0
            for c in contacts:
                if db.save_contact(c):
                    migrated_contacts += 1
            print(f"[Contacts] Successfully migrated {migrated_contacts}/{len(contacts)} contacts to Neon PostgreSQL.")
        except Exception as e:
            print(f"[Contacts Error]: {e}")

    print("\n" + "=" * 60)
    print(">> All data migration to Neon PostgreSQL completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    migrate()

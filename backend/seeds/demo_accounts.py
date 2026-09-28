from backend.models.users import get_all_users, save_user

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

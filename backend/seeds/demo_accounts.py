from werkzeug.security import generate_password_hash
from backend.models.users import get_all_users, save_user, update_user

def _seed_demo_accounts():
    """
    Ensure standard demo accounts (Rider, Patient, Doctor, Lab, Pharmacy, Premium OPD)
    exist in the system with cryptographically secure hashed passwords.
    """
    demo_accounts = [
        {
            'id': 'USR-DOC-001',
            'email': 'doctor@nhealth.in',
            'phone': '9876543210',
            'role': 'doctor',
            'password': generate_password_hash('password123'),
            'name': 'Dr. Arjun Reddy',
            'doctor_id': 'DOC78456',
            'qualification': 'MBBS, MD (General Medicine)',
            'specialization': 'General Physician',
            'experience': '8+ Years',
            'reg_number': 'APMC/12345',
            'clinic_name': 'Nhealth Prime Care Center',
            'city': 'Vijayawada',
            'state': 'Andhra Pradesh',
            'pincode': '520002',
            'address': 'Governorpet, Vijayawada, Andhra Pradesh',
            'is_active': True
        },
        {
            'id': 'USR-PAT-001',
            'email': 'patient@nhealth.in',
            'phone': '9123456780',
            'role': 'patient',
            'password': generate_password_hash('password123'),
            'name': 'Ananya Sharma',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'pincode': '500081',
            'age': 26,
            'dob': '2000-04-12',
            'gender': 'Female',
            'blood_group': 'A+',
            'address': 'Madhapur, Hyderabad, Telangana - 500081',
            'is_active': True
        },
        {
            'id': 'USR-RIDER-001',
            'email': 'rider@nhealth.in',
            'phone': '9876543222',
            'role': 'rider',
            'password': generate_password_hash('password123'),
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
        },
        {
            'id': 'USR-LAB-001',
            'email': 'lab@nhealth.in',
            'phone': '9876543299',
            'role': 'lab',
            'password': generate_password_hash('password123'),
            'name': 'Apollo Diagnostics & Pathology Lab',
            'owner_name': 'Dr. K. Srinivas Rao',
            'specialization': 'Diagnostic Pathology & Blood Tests',
            'clinic_name': 'Apollo Diagnostics & Pathology Lab',
            'reg_number': 'AP-LAB-2026-001',
            'city': 'Vijayawada',
            'state': 'Andhra Pradesh',
            'pincode': '520010',
            'address': 'MG Road, Vijayawada, Andhra Pradesh',
            'is_active': True
        },
        {
            'id': 'USR-PHA-001',
            'email': 'pharmacy@nhealth.in',
            'phone': '9876543290',
            'role': 'pharmacy',
            'password': generate_password_hash('password123'),
            'name': 'Sai Medicals',
            'owner_name': 'Sai Medicals & Pharmacy',
            'specialization': 'Doorstep E-Pharmacy',
            'clinic_name': 'Sai Medicals',
            'reg_number': 'PHA-000123',
            'gst_number': '37CCCC1234A1Z3',
            'city': 'Narasaraopeta',
            'state': 'Andhra Pradesh',
            'pincode': '522601',
            'address': 'Main Road, Near Gandhi Chowk, Narasaraopeta, Andhra Pradesh',
            'is_active': True
        },
        {
            'id': 'USR-OPD-7788',
            'email': 'opd@nhealth.in',
            'phone': '9988001122',
            'role': 'premium-opd',
            'password': generate_password_hash('password123'),
            'name': 'Shiva Pendala',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'age': 28,
            'gender': 'Male',
            'blood_group': 'O+',
            'address': 'Flat 402, Royal Residency, Madhapur, Hyderabad',
            'membership_id': 'NH-OPD-2026-7788',
            'membership_plan': 'Premium OPD Platinum',
            'membership_status': 'Active',
            'is_active': True
        }
    ]

    try:
        existing_users = get_all_users()
        existing_by_email = {u.get('email', '').lower(): u for u in existing_users if u.get('email')}
        existing_by_phone = {str(u.get('phone', '')): u for u in existing_users if u.get('phone')}

        for acc in demo_accounts:
            email = acc['email'].lower()
            phone = str(acc['phone'])
            match = existing_by_email.get(email) or existing_by_phone.get(phone)
            if not match:
                save_user(acc)
            else:
                # Upgrade legacy plain text password to secure hash if necessary
                stored_pwd = match.get('password', '')
                if not stored_pwd.startswith(('pbkdf2:sha256:', 'scrypt:', 'argon2:')):
                    update_user(match['id'], {'password': generate_password_hash('password123')})
    except Exception as e:
        print(f"[DB Seed Error]: {e}")

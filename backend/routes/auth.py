"""
Authentication routes: login, signup, logout (UI pages and APIs).
"""

import re
import uuid
from datetime import datetime, date
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash

from backend.data import SERVICES, AP_LOCATIONS, STATS
from backend.models import get_all_users, save_user, update_user
from backend.services import (
    verify_password,
    is_rate_limited,
    record_failed_attempt,
    clear_failed_attempts,
    ensure_patient_fields
)

auth_bp = Blueprint('auth', __name__)


# ==================== PAGE ROUTES ====================

@auth_bp.route('/login')
def login_page():
    """Render the Login page."""
    role = request.args.get('role', 'patient')
    if role == 'lab':
        return redirect(url_for('auth.login_lab_page'))
    if role == 'rider':
        return redirect(url_for('auth.login_rider_page'))
    return render_template('auth/login.html', role=role, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/login/lab')
@auth_bp.route('/lab/login')
def login_lab_page():
    """Render dedicated Lab Login page."""
    return render_template('auth/login_lab.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/login/pharmacy')
@auth_bp.route('/pharmacy/login')
def login_pharmacy_page():
    """Render Login page pre-configured for Pharmacy Partner."""
    return render_template('auth/login.html', role='pharmacy', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/login/rider')
@auth_bp.route('/rider/login')
def login_rider_page():
    """Render dedicated Rider Login page."""
    return render_template('auth/login_rider.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/signup')
def signup_page():
    """Render the Signup page (defaults to patient or uses role query)."""
    role = request.args.get('role', 'patient')
    if role == 'lab':
        return redirect(url_for('auth.signup_lab_page'))
    if role == 'rider':
        return redirect(url_for('auth.signup_rider_page'))
    if role in ['doctor', 'partner']:
        return render_template('auth/signup_partner.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)
    return render_template('auth/signup_patient.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/signup/patient')
def signup_patient_page():
    """Render Patient Sign Up page."""
    return render_template('auth/signup_patient.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/signup/doctor')
@auth_bp.route('/signup/partner')
def signup_doctor_page():
    """Render Doctor / Partner Sign Up page."""
    return render_template('auth/signup_partner.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/signup/lab')
@auth_bp.route('/lab/signup')
def signup_lab_page():
    """Render dedicated Lab Sign Up page."""
    return render_template('auth/signup_lab.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/signup/rider')
@auth_bp.route('/rider/signup')
def signup_rider_page():
    """Render dedicated Rider Sign Up page."""
    return render_template('auth/signup_rider.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@auth_bp.route('/logout')
def app_logout():
    """Log out user, clear session, and redirect cleanly."""
    user = session.get('user')
    was_rider = bool(user and user.get('role') == 'rider') or request.args.get('role') == 'rider'
    session.clear()
    if was_rider:
        return redirect(url_for('auth.login_rider_page'))
    return redirect(url_for('auth.login_page'))


# ==================== AUTH API ROUTES ====================

@auth_bp.route('/api/auth/signup', methods=['POST'])
def auth_signup():
    """Handle new patient or doctor/partner account registration with security validation."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        role = data.get('role', 'patient').strip().lower()
        name = (data.get('name', '') or data.get('lab_name', '')).strip()
        owner_name = (data.get('owner_name') or data.get('ownerName', '')).strip()
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', 'Andhra Pradesh').strip()
        pincode = data.get('pincode', '').strip()
        address = (data.get('address') or data.get('full_address', '')).strip()
        dob = (data.get('dob') or data.get('date_of_birth', '')).strip()
        gender = (data.get('gender') or 'Male').strip()
        reg_number = (data.get('reg_number') or data.get('registrationNumber', '')).strip()
        gst_number = (data.get('gst_number') or data.get('gstNumber', '')).strip()
        password = data.get('password', '').strip()

        # Calculate age if dob is given
        calculated_age = None
        if dob:
            try:
                birth_date = datetime.strptime(dob, '%Y-%m-%d')
                today = date.today()
                calculated_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            except Exception:
                try:
                    for fmt in ('%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d'):
                        try:
                            birth_date = datetime.strptime(dob, fmt)
                            today = date.today()
                            calculated_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                            dob = birth_date.strftime('%Y-%m-%d')
                            break
                        except ValueError:
                            continue
                except Exception:
                    pass
        if calculated_age is None:
            if str(data.get('age', '')).isdigit():
                calculated_age = int(data.get('age'))
            else:
                calculated_age = 30

        # Required fields validation
        if not name or not phone or not password:
            return jsonify({
                "status": "error",
                "message": "Full Name / Lab Name, Mobile Number, and Password are required."
            }), 400

        # Clean phone and validate 10 digits
        clean_phone = re.sub(r'\D', '', phone)
        if len(clean_phone) != 10:
            return jsonify({
                "status": "error",
                "message": "Please enter a valid 10-digit mobile number."
            }), 400

        # Rider specific 2 mandatory contact numbers & validation
        clean_sec_phone = ''
        location_type = data.get('location_type', 'city').strip().lower()
        town_village = (data.get('town_village') or data.get('city') or city).strip()

        if role == 'rider':
            secondary_phone = (data.get('secondary_phone') or data.get('emergency_phone') or '').strip()
            clean_sec_phone = re.sub(r'\D', '', secondary_phone)
            if len(clean_sec_phone) != 10:
                return jsonify({
                    "status": "error",
                    "message": "Secondary / Alternate Contact Number is mandatory and must be a valid 10-digit number."
                }), 400
            if clean_phone == clean_sec_phone:
                return jsonify({
                    "status": "error",
                    "message": "Primary and Secondary contact numbers must be different."
                }), 400
            if not data.get('has_individual_photo'):
                return jsonify({
                    "status": "error",
                    "message": "Individual Photo is mandatory for rider verification."
                }), 400

        # Password minimum length check
        if len(password) < 6:
            return jsonify({
                "status": "error",
                "message": "Password must be at least 6 characters long."
            }), 400

        users = get_all_users()

        # Check existing user
        if any(u.get('phone') == clean_phone or (email and u.get('email', '').lower() == email) for u in users):
            return jsonify({
                "status": "error",
                "message": "An account with this mobile number or email already exists. Please login."
            }), 409

        user_id = f"USR-{role[:3].upper()}-{datetime.now().strftime('%y%m')}-{uuid.uuid4().hex[:4].upper()}"

        user_record = {
            "id": user_id,
            "role": role,
            "name": name,
            "owner_name": owner_name,
            "email": email,
            "phone": clean_phone,
            "secondary_phone": clean_sec_phone,
            "whatsapp": data.get('whatsapp', clean_phone).strip(),
            "specialization": data.get('specialization', 'Diagnostic Pathology' if role == 'lab' else ''),
            "clinic_name": data.get('clinic_name', name if role == 'lab' else ''),
            "reg_number": reg_number,
            "gst_number": gst_number,
            "city": city or "Vijayawada",
            "state": state,
            "location_type": location_type,
            "town_village": town_village,
            "pincode": pincode,
            "age": calculated_age,
            "dob": dob,
            "gender": gender,
            "blood_group": data.get('blood_group', 'O+'),
            "address": address or f"{town_village or city or 'Vijayawada'}, {state}",
            "vehicle_type": data.get('vehicle_type', data.get('vehicleType', 'Motorcycle (Two-Wheeler)')),
            "vehicle_number": data.get('vehicle_number', data.get('vehicleNumber', '')),
            "is_online": True,
            "rating": "5.0",
            "has_individual_photo": data.get('has_individual_photo', False),
            "has_family_photo": data.get('has_family_photo', False),
            "has_police_noc": data.get('has_police_noc', False),
            "payment_mode": "Online Only",
            "extra_data": {
                "secondary_phone": clean_sec_phone,
                "location_type": location_type,
                "town_village": town_village,
                "has_individual_photo": data.get('has_individual_photo', False),
                "has_family_photo": data.get('has_family_photo', False),
                "has_police_noc": data.get('has_police_noc', False),
                "individual_photo_name": data.get('individual_photo_name'),
                "family_photo_name": data.get('family_photo_name'),
                "police_noc_name": data.get('police_noc_name')
            },
            "password": generate_password_hash(password),
            "created_at": datetime.now().isoformat()
        }

        save_user(user_record)

        # Set session for seamless login
        clean_user = {k: v for k, v in user_record.items() if k != 'password'}
        ensure_patient_fields(clean_user)
        session['user_id'] = user_record["id"]
        session['user'] = clean_user

        if role in ['pharmacy', 'pharma']:
            redirect_url = '/pharmacy/dashboard'
        elif role == 'lab':
            redirect_url = '/lab/dashboard'
        elif role == 'rider':
            redirect_url = '/rider/dashboard'
        elif role == 'patient':
            redirect_url = '/patient/dashboard'
        else:
            redirect_url = '/'

        return jsonify({
            "status": "success",
            "message": f"Account successfully created! Welcome to Nhealth, {name}.",
            "user": clean_user,
            "redirect": redirect_url
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Sign up failed: {str(e)}"
        }), 500


@auth_bp.route('/api/auth/login', methods=['POST'])
def auth_login():
    """Handle secure authentication via credentials with rate-limiting."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        identifier = data.get('identifier', '').strip()
        password = data.get('password', '').strip()
        role = data.get('role', '')

        client_ip = request.remote_addr or 'unknown'
        rate_key = f"{client_ip}:{identifier}"

        # Rate-limiting / Brute-force lockout check
        is_limited, wait_time = is_rate_limited(rate_key)
        if is_limited:
            return jsonify({
                "status": "error",
                "message": f"Too many failed login attempts. For security reasons, please wait {wait_time} seconds before trying again."
            }), 429

        if not identifier:
            return jsonify({
                "status": "error",
                "message": "Please enter your Mobile Number or Email."
            }), 400

        if not password:
            return jsonify({
                "status": "error",
                "message": "Please enter your Password."
            }), 400

        users = get_all_users()
        identifier_lower = identifier.lower()
        clean_digits = re.sub(r'\D', '', identifier)

        # Find matching user
        matched = None
        for u in users:
            u_email = u.get('email', '').lower()
            u_phone = re.sub(r'\D', '', str(u.get('phone', '')))
            if (u_email and u_email == identifier_lower) or (clean_digits and u_phone == clean_digits):
                matched = u
                break

        # Guaranteed fallback for official demo credentials
        if not matched:
            if identifier_lower in ['pharmacy@nhealth.in', 'pharma@gmail.com', 'pharma@nhealth.in', 'saimedicals@gmail.com'] or clean_digits in ['9876543290', '9988776655']:
                matched = {
                    "id": "USR-PHA-001",
                    "role": "pharmacy",
                    "name": "Sai Medicals",
                    "owner_name": "Sai Medicals & Pharmacy",
                    "email": identifier_lower if '@' in identifier_lower else "pharmacy@nhealth.in",
                    "phone": clean_digits or "9876543290",
                    "whatsapp": clean_digits or "9876543290",
                    "specialization": "Doorstep E-Pharmacy",
                    "clinic_name": "Sai Medicals",
                    "reg_number": "PHA-000123",
                    "gst_number": "37CCCC1234A1Z3",
                    "city": "Narasaraopeta",
                    "state": "Andhra Pradesh",
                    "pincode": "522601",
                    "address": "Main Road, Near Gandhi Chowk, Narasaraopeta",
                    "password": "password123",
                    "created_at": "2026-01-15T10:00:00"
                }
            elif identifier_lower in ['lab@nhealth.in', 'lab@gmail.com'] or clean_digits in ['9876543299']:
                matched = {
                    "id": "USR-LAB-001",
                    "role": "lab",
                    "name": "Apollo Diagnostics & Pathology Lab",
                    "owner_name": "Dr. K. Srinivas Rao",
                    "email": identifier_lower if '@' in identifier_lower else "lab@nhealth.in",
                    "phone": clean_digits or "9876543299",
                    "whatsapp": clean_digits or "9876543299",
                    "specialization": "Diagnostic Pathology & Blood Tests",
                    "clinic_name": "Apollo Diagnostics & Pathology Lab",
                    "reg_number": "AP-LAB-2026-001",
                    "city": "Vijayawada",
                    "password": "password123"
                }
            elif identifier_lower in ['priya.sharma@nhealth.in', 'dr.priya@nhealth.in', 'priya@gmail.com', 'priya@nhealth.in', 'priya'] or clean_digits in ['9848011223']:
                matched = {
                    "id": "USR-DOC-002",
                    "role": "doctor",
                    "name": "Dr. Priya Sharma",
                    "doctor_id": "DOC-NH-74892",
                    "qualification": "MBBS, MD (General Medicine)",
                    "specialization": "General Physician & Internal Medicine",
                    "experience": "9+ Years",
                    "reg_number": "APMC/74892",
                    "clinic_name": "Nhealth Prime Care Center",
                    "email": identifier_lower if '@' in identifier_lower else "priya.sharma@nhealth.in",
                    "phone": clean_digits or "9848011223",
                    "city": "Vijayawada",
                    "password": "password123"
                }
            elif identifier_lower in ['doctor@nhealth.in', 'doctor@gmail.com', 'dr.arjun@nhealth.in'] or clean_digits in ['9876543210']:
                matched = {
                    "id": "USR-DOC-001",
                    "role": "doctor",
                    "name": "Dr. Arjun Reddy",
                    "doctor_id": "DOC78456",
                    "qualification": "MBBS, MD (General Medicine)",
                    "specialization": "General Physician",
                    "experience": "8+ Years",
                    "reg_number": "APMC/12345",
                    "email": identifier_lower if '@' in identifier_lower else "doctor@nhealth.in",
                    "phone": clean_digits or "9876543210",
                    "city": "Vijayawada",
                    "password": "password123"
                }
            elif identifier_lower in ['patient@nhealth.in', 'patient@gmail.com'] or clean_digits in ['9123456780']:
                matched = {
                    "id": "USR-PAT-001",
                    "role": "patient",
                    "name": "Suresh Kumar",
                    "email": identifier_lower if '@' in identifier_lower else "patient@nhealth.in",
                    "phone": clean_digits or "9123456780",
                    "city": "Visakhapatnam",
                    "password": "password123"
                }

        if not matched or not verify_password(matched.get('password', ''), password):
            record_failed_attempt(rate_key)
            return jsonify({
                "status": "error",
                "message": "Invalid mobile number/email or password. Please check your credentials."
            }), 401

        # Clear failed attempts on successful login
        clear_failed_attempts(rate_key)

        # Upgrade legacy plain-text password to secure hash if needed
        if not matched.get('password', '').startswith(('pbkdf2:sha256:', 'scrypt:', 'argon2:')):
            update_user(matched['id'], {'password': generate_password_hash(password)})

        clean_user = {k: v for k, v in matched.items() if k != 'password'}
        ensure_patient_fields(clean_user)
        session['user_id'] = matched['id']
        session['user'] = clean_user

        user_role = clean_user.get('role', '') or role or 'patient'
        if user_role in ['pharmacy', 'pharma'] or role in ['pharmacy', 'pharma']:
            redirect_url = '/pharmacy/dashboard'
        elif user_role == 'lab' or role == 'lab':
            redirect_url = '/lab/dashboard'
        elif user_role == 'rider' or role == 'rider':
            redirect_url = '/rider/dashboard'
        elif user_role == 'doctor' or role == 'doctor':
            redirect_url = '/doctor/dashboard'
        else:
            redirect_url = '/patient/dashboard'

        return jsonify({
            "status": "success",
            "message": f"Welcome back, {clean_user['name']}!",
            "user": clean_user,
            "redirect": redirect_url
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Login failed: {str(e)}"
        }), 500


@auth_bp.route('/api/auth/logout', methods=['POST', 'GET'])
def auth_logout():
    """Clear session on logout."""
    session.clear()
    return jsonify({
        "status": "success",
        "message": "Logged out successfully"
    }), 200

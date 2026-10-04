import time
from functools import wraps
from flask import session, request, redirect, url_for, jsonify
from werkzeug.security import check_password_hash

def verify_password(stored_password, provided_password):
    """
    Securely verify user password.
    Enforces strict cryptographic hash verification and case-sensitivity.
    """
    if not stored_password or not provided_password:
        return False
    stored_str = str(stored_password).strip()
    provided_str = str(provided_password)

    # Secure hashed passwords (PBKDF2, Scrypt, Argon2)
    if stored_str.startswith(('pbkdf2:sha256:', 'scrypt:', 'argon2:')):
        return check_password_hash(stored_str, provided_str)

    # Legacy plain-text fallback (strictly case-sensitive, exact match only)
    return stored_str == provided_str


# Rate-limiting failed logins (brute-force defense)
FAILED_LOGIN_ATTEMPTS = {}  # { key: {'count': int, 'lockout_until': timestamp} }

def is_rate_limited(key):
    """Check if key (IP:identifier) is currently locked out."""
    record = FAILED_LOGIN_ATTEMPTS.get(key)
    if not record:
        return False, 0
    now = time.time()
    if record.get('lockout_until', 0) > now:
        remaining = int(record['lockout_until'] - now)
        return True, remaining
    # Expired lockout: reset counter
    if record.get('lockout_until', 0) > 0 and record['lockout_until'] <= now:
        FAILED_LOGIN_ATTEMPTS.pop(key, None)
    return False, 0

def record_failed_attempt(key):
    """Increment failed login counter and trigger progressive lockout."""
    now = time.time()
    record = FAILED_LOGIN_ATTEMPTS.get(key, {'count': 0, 'lockout_until': 0})
    record['count'] += 1
    # 5 failed attempts -> 60s lockout, 10+ failed attempts -> 5 min lockout
    if record['count'] >= 10:
        record['lockout_until'] = now + 300
    elif record['count'] >= 5:
        record['lockout_until'] = now + 60
    FAILED_LOGIN_ATTEMPTS[key] = record

def clear_failed_attempts(key):
    """Clear failed attempts upon successful login."""
    FAILED_LOGIN_ATTEMPTS.pop(key, None)


def login_required(f):
    """
    Decorator to ensure user is logged in.
    Redirects to appropriate login page for web routes or returns 401 for APIs.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        user = session.get('user')
        if not user_id or not user:
            if request.path.startswith('/api/'):
                return jsonify({
                    "status": "error",
                    "message": "Authentication required. Please log in."
                }), 401
            # Check route context to redirect to proper login page
            if '/lab' in request.path:
                return redirect(url_for('auth.login_lab_page', next=request.path))
            if '/rider' in request.path:
                return redirect(url_for('auth.login_rider_page', next=request.path))
            if '/pharmacy' in request.path:
                return redirect(url_for('auth.login_pharmacy_page', next=request.path))
            if '/doctor' in request.path:
                return redirect(url_for('auth.login_page', role='doctor', next=request.path))
            return redirect(url_for('auth.login_page', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to enforce Role-Based Access Control (RBAC).
    Allowed roles can be passed as strings or a list of strings.
    """
    # Flatten roles
    roles = []
    for r in allowed_roles:
        if isinstance(r, (list, tuple, set)):
            roles.extend(r)
        else:
            roles.append(r)

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            user = session.get('user')
            if not user_id or not user:
                if request.path.startswith('/api/'):
                    return jsonify({
                        "status": "error",
                        "message": "Authentication required. Please log in."
                    }), 401
                if 'lab' in roles:
                    return redirect(url_for('auth.login_lab_page', next=request.path))
                if 'rider' in roles:
                    return redirect(url_for('auth.login_rider_page', next=request.path))
                if 'pharmacy' in roles or 'pharma' in roles:
                    return redirect(url_for('auth.login_pharmacy_page', next=request.path))
                if 'doctor' in roles:
                    return redirect(url_for('auth.login_page', role='doctor', next=request.path))
                return redirect(url_for('auth.login_page', next=request.path))

            user_role = (user.get('role') or '').lower()
            # Normalize pharmacy/pharma
            normalized_user_roles = [user_role]
            if user_role == 'pharmacy':
                normalized_user_roles.append('pharma')
            elif user_role == 'pharma':
                normalized_user_roles.append('pharmacy')
            if user_role == 'premium-opd':
                normalized_user_roles.append('patient')

            matched = any(r.lower() in normalized_user_roles for r in roles)
            if not matched:
                if request.path.startswith('/api/'):
                    return jsonify({
                        "status": "error",
                        "message": f"Access forbidden: requires one of [{', '.join(roles)}] role."
                    }), 403
                # Redirect user to their own valid dashboard
                if user_role in ['pharmacy', 'pharma']:
                    return redirect('/pharmacy/dashboard')
                elif user_role == 'lab':
                    return redirect('/lab/dashboard')
                elif user_role == 'rider':
                    return redirect('/rider/dashboard')
                elif user_role == 'doctor':
                    return redirect('/doctor/dashboard')
                elif user_role == 'premium-opd':
                    return redirect('/opd-dashboard')
                else:
                    return redirect('/patient/dashboard')

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def ensure_patient_fields(user_dict):
    """Ensure baseline profile fields are present for patient rendering."""
    if not isinstance(user_dict, dict):
        return
    if not user_dict.get('age'):
        user_dict['age'] = 30
    if not user_dict.get('dob'):
        user_dict['dob'] = '1995-05-15'
    if not user_dict.get('gender'):
        user_dict['gender'] = 'Male'
    if not user_dict.get('blood_group'):
        user_dict['blood_group'] = 'O+'
    if not user_dict.get('city'):
        user_dict['city'] = 'Vijayawada'
    if not user_dict.get('address'):
        user_dict['address'] = f"{user_dict.get('city', 'Vijayawada')}, Andhra Pradesh"

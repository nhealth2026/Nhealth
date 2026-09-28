import time
from werkzeug.security import check_password_hash

def verify_password(stored_password, provided_password):
    if not stored_password or not provided_password:
        return False
    stored_clean = str(stored_password).strip()
    provided_clean = str(provided_password).strip()
    if stored_clean.startswith(('pbkdf2:sha256:', 'scrypt:', 'argon2:')):
        if check_password_hash(stored_clean, provided_password):
            return True
        if check_password_hash(stored_clean, provided_clean):
            return True
        if check_password_hash(stored_clean, provided_clean.lower()):
            return True
        return False
    return stored_clean == provided_clean or stored_clean.lower() == provided_clean.lower()

# Rate-limiting failed logins (security)
FAILED_LOGIN_ATTEMPTS = {}  # { key: {'count': int, 'lockout_until': timestamp} }

def is_rate_limited(key):
    record = FAILED_LOGIN_ATTEMPTS.get(key)
    if not record:
        return False, 0
    now = time.time()
    if record.get('lockout_until', 0) > now:
        remaining = int(record['lockout_until'] - now)
        return True, remaining
    return False, 0

def record_failed_attempt(key):
    now = time.time()
    record = FAILED_LOGIN_ATTEMPTS.get(key, {'count': 0, 'lockout_until': 0})
    record['count'] += 1
    if record['count'] >= 5:
        record['lockout_until'] = now + 30  # 30-second lockout after 5 failed attempts
    FAILED_LOGIN_ATTEMPTS[key] = record

def clear_failed_attempts(key):
    FAILED_LOGIN_ATTEMPTS.pop(key, None)

def ensure_patient_fields(user_dict):
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

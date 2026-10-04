from flask import session
from backend.models.users import get_all_users
from .auth_helpers import ensure_patient_fields

def get_current_patient():
    """
    Retrieve current logged-in patient from authenticated session.
    Returns None if not authenticated (prevents data leakage).
    """
    user_id = session.get('user_id')
    if user_id:
        users = get_all_users()
        for u in users:
            if u.get('id') == user_id:
                clean = {k: v for k, v in u.items() if k != 'password'}
                ensure_patient_fields(clean)
                return clean
    
    if 'user' in session:
        clean = dict(session['user'])
        ensure_patient_fields(clean)
        return clean
    
    return None

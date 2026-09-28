from flask import session
from backend.models.users import get_all_users
from .auth_helpers import ensure_patient_fields

def get_current_patient():
    """Retrieve current logged in patient from session or fallback to latest registered patient."""
    user_id = session.get('user_id')
    users = get_all_users()
    
    if user_id:
        for u in users:
            if u.get('id') == user_id:
                clean = {k: v for k, v in u.items() if k != 'password'}
                ensure_patient_fields(clean)
                return clean
    
    if 'user' in session:
        clean = dict(session['user'])
        ensure_patient_fields(clean)
        return clean
    
    # Fallback to the latest patient registered in users.json so there are never dummy placeholder names
    patients = [u for u in users if u.get('role') == 'patient']
    if patients:
        latest = patients[-1]
        clean = {k: v for k, v in latest.items() if k != 'password'}
        ensure_patient_fields(clean)
        return clean
        
    return {
        "id": "USR-PAT-NEW",
        "name": "Valued Patient",
        "email": "patient@nhealth.in",
        "phone": "9876543210",
        "city": "Vijayawada",
        "age": 32,
        "gender": "Male",
        "blood_group": "O+",
        "address": "Vijayawada, Andhra Pradesh"
    }

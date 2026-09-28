"""
User profile management APIs.
"""

from datetime import datetime, date
from flask import Blueprint, request, jsonify, session
from backend.models import get_all_users, update_user
from backend.services import get_current_patient, ensure_patient_fields

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/api/user/profile', methods=['GET', 'POST'])
def user_profile():
    """Retrieve or update logged-in patient profile."""
    try:
        if request.method == 'GET':
            patient = get_current_patient()
            return jsonify({"status": "success", "user": patient}), 200

        # POST: update profile
        data = request.get_json() if request.is_json else request.form.to_dict()
        user_id = data.get('id') or session.get('user_id')
        
        users = get_all_users()
        target_user = None
        if user_id:
            for u in users:
                if u.get('id') == user_id:
                    target_user = u
                    break
        if not target_user and users:
            target_user = users[-1]
            user_id = target_user['id']

        updates = {}
        if 'name' in data and data['name'].strip():
            updates['name'] = data['name'].strip()
        if 'phone' in data and data['phone'].strip():
            updates['phone'] = data['phone'].strip()
        if 'email' in data and data['email'].strip():
            updates['email'] = data['email'].strip()
        if 'city' in data and data['city'].strip():
            updates['city'] = data['city'].strip()
        if 'age' in data:
            try:
                updates['age'] = int(data['age'])
            except (ValueError, TypeError):
                pass
        if 'dob' in data and data['dob'].strip():
            updates['dob'] = data['dob'].strip()
            try:
                birth_date = datetime.strptime(data['dob'].strip(), '%Y-%m-%d')
                today = date.today()
                updates['age'] = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            except Exception:
                pass
        if 'gender' in data and data['gender'].strip():
            updates['gender'] = data['gender'].strip()
        if 'blood_group' in data and data['blood_group'].strip():
            updates['blood_group'] = data['blood_group'].strip()
        if 'address' in data and data['address'].strip():
            updates['address'] = data['address'].strip()

        if user_id and updates:
            update_user(user_id, updates)
            for k, v in updates.items():
                target_user[k] = v
            clean_user = {k: v for k, v in target_user.items() if k != 'password'}
            ensure_patient_fields(clean_user)
            session['user_id'] = clean_user['id']
            session['user'] = clean_user
            return jsonify({
                "status": "success",
                "message": "Patient profile updated successfully!",
                "user": clean_user
            }), 200
        
        return jsonify({"status": "error", "message": "No profile updates provided."}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to update profile: {str(e)}"}), 500

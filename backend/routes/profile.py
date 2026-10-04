"""
User profile management APIs.
Protected with session authentication (prevents IDOR and unauthorized profile modification).
"""

from datetime import datetime, date
from flask import Blueprint, request, jsonify, session
from backend.models import get_all_users, update_user
from backend.services import get_current_patient, ensure_patient_fields, login_required

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/api/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """Retrieve or update logged-in patient profile."""
    try:
        if request.method == 'GET':
            patient = get_current_patient()
            if not patient:
                return jsonify({"status": "error", "message": "User profile not found."}), 404
            return jsonify({"status": "success", "user": patient}), 200

        # POST: update profile of authenticated user only
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"status": "error", "message": "Authentication required."}), 401

        users = get_all_users()
        target_user = None
        for u in users:
            if u.get('id') == user_id:
                target_user = u
                break

        if not target_user:
            return jsonify({"status": "error", "message": "User account not found."}), 404

        data = request.get_json() if request.is_json else request.form.to_dict()
        updates = {}
        if 'name' in data and data['name'].strip():
            updates['name'] = data['name'].strip()
        if 'phone' in data and data['phone'].strip():
            updates['phone'] = data['phone'].strip()
        if 'email' in data and data['email'].strip():
            updates['email'] = data['email'].strip().lower()
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

        if updates:
            update_user(user_id, updates)
            for k, v in updates.items():
                target_user[k] = v
            clean_user = {k: v for k, v in target_user.items() if k != 'password'}
            ensure_patient_fields(clean_user)
            session['user'] = clean_user
            return jsonify({
                "status": "success",
                "message": "Patient profile updated successfully!",
                "user": clean_user
            }), 200
        
        return jsonify({"status": "error", "message": "No profile updates provided."}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to update profile: {str(e)}"}), 500

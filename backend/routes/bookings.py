"""
General booking and contact inquiry APIs.
"""

import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.models import save_booking, save_contact

bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('/api/book', methods=['POST'])
def book_appointment():
    """Handle appointment / home healthcare booking."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()

        required_fields = ['name', 'phone', 'service', 'city']
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing)}"
            }), 400

        # Validate phone
        phone = data.get('phone', '').strip()
        if len(phone) < 10:
            return jsonify({
                "status": "error",
                "message": "Please provide a valid 10-digit phone number."
            }), 400

        booking_id = f"NH-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        booking_record = {
            "booking_id": booking_id,
            "created_at": datetime.now().isoformat(),
            "name": data.get('name', '').strip(),
            "phone": phone,
            "email": data.get('email', '').strip(),
            "service": data.get('service', '').strip(),
            "city": data.get('city', '').strip(),
            "address": data.get('address', '').strip(),
            "preferred_date": data.get('date', datetime.now().strftime('%Y-%m-%d')),
            "time_slot": data.get('time_slot', 'Morning (9:00 AM - 1:00 PM)'),
            "notes": data.get('notes', '').strip(),
            "status": "Confirmed"
        }

        save_booking(booking_record)

        return jsonify({
            "status": "success",
            "message": f"Thank you {booking_record['name']}! Your home healthcare request has been confirmed.",
            "booking_id": booking_id,
            "details": {
                "service": booking_record['service'],
                "city": booking_record['city'],
                "date": booking_record['preferred_date'],
                "slot": booking_record['time_slot']
            }
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500


@bookings_bp.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle general inquiries and contact requests from website."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '').strip()
        subject = data.get('subject', 'General Inquiry').strip()
        message = data.get('message', '').strip()

        if not name or not phone:
            return jsonify({
                "status": "error",
                "message": "Full name and phone number are required."
            }), 400

        contact_entry = {
            "id": f"INQ-{datetime.now().strftime('%y%m%d')}-{uuid.uuid4().hex[:4].upper()}",
            "name": name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message,
            "created_at": datetime.now().isoformat(),
            "status": "new"
        }

        save_contact(contact_entry)

        return jsonify({
            "status": "success",
            "message": f"Thank you, {name}! Your message regarding '{subject}' has been received. Our support team will get back to you shortly."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to submit: {str(e)}"
        }), 500

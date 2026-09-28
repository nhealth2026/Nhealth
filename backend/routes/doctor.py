"""
Doctor partner dashboard routes.
"""

from flask import Blueprint, render_template, session
from backend.data import SERVICES, AP_LOCATIONS, STATS

doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/doctor/dashboard')
@doctor_bp.route('/dashboard/doctor')
@doctor_bp.route('/doctor')
def doctor_dashboard():
    """Render Doctor Partner Dashboard matching reference design."""
    user = session.get('user')
    if not user or user.get('role') != 'doctor':
        user = {
            "id": "USR-DOC-001",
            "name": "Dr. Arjun Reddy",
            "doctor_id": "DOC78456",
            "qualification": "MBBS, MD (General Medicine)",
            "specialization": "General Physician",
            "experience": "8+ Years",
            "reg_number": "APMC/12345",
            "role": "doctor",
            "city": "Vijayawada",
            "phone": "9876543210",
            "email": "doctor@nhealth.in"
        }
    return render_template('dashboards/doctor_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)

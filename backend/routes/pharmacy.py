"""
Pharmacy partner dashboard routes.
"""

from flask import Blueprint, render_template, session
from backend.data import SERVICES, AP_LOCATIONS, STATS

pharmacy_bp = Blueprint('pharmacy', __name__)


@pharmacy_bp.route('/pharmacy/dashboard')
@pharmacy_bp.route('/dashboard/pharmacy')
@pharmacy_bp.route('/pharma/dashboard')
@pharmacy_bp.route('/pharmacy')
def pharmacy_dashboard():
    """Render Pharmacy Partner Dashboard matching reference design."""
    user = session.get('user')
    if not user or user.get('role') != 'pharmacy':
        user = {
            "id": "PHA-000123",
            "name": "Sai Medicals",
            "owner_name": "Sai Medicals & Pharmacy",
            "role": "pharmacy",
            "city": "Narasaraopeta",
            "phone": "9876543290",
            "email": "pharmacy@nhealth.in"
        }
    return render_template('dashboards/pharmacy_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)

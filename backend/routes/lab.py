"""
Lab partner dashboard routes.
"""

from flask import Blueprint, render_template, session
from backend.data import SERVICES, AP_LOCATIONS, STATS

lab_bp = Blueprint('lab', __name__)


@lab_bp.route('/lab/dashboard')
@lab_bp.route('/dashboard/lab')
def lab_dashboard():
    """Render Lab Partner Dashboard."""
    user = session.get('user')
    if not user:
        user = {
            "id": "LAB-AP-2026",
            "name": "Apollo Diagnostics & Pathology Lab",
            "owner_name": "Dr. K. Srinivas Rao",
            "role": "lab",
            "city": "Vijayawada",
            "phone": "9876543210",
            "email": "lab@nhealth.in"
        }
    return render_template('dashboards/lab_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)

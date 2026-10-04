"""
Doctor partner dashboard routes.
Protected with role-based access control.
"""

from flask import Blueprint, render_template, session
from backend.data import SERVICES, AP_LOCATIONS, STATS
from backend.services import role_required

doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/doctor/dashboard')
@doctor_bp.route('/dashboard/doctor')
@doctor_bp.route('/doctor')
@role_required('doctor')
def doctor_dashboard():
    """Render Doctor Partner Dashboard matching reference design."""
    user = session.get('user')
    return render_template('dashboards/doctor_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)

"""
Pharmacy partner dashboard routes.
Protected with role-based access control.
"""

from flask import Blueprint, render_template, session
from backend.data import SERVICES, AP_LOCATIONS, STATS
from backend.services import role_required

pharmacy_bp = Blueprint('pharmacy', __name__)


@pharmacy_bp.route('/pharmacy/dashboard')
@pharmacy_bp.route('/dashboard/pharmacy')
@pharmacy_bp.route('/pharma/dashboard')
@pharmacy_bp.route('/pharmacy')
@role_required('pharmacy', 'pharma')
def pharmacy_dashboard():
    """Render Pharmacy Partner Dashboard matching reference design."""
    user = session.get('user')
    return render_template('dashboards/pharmacy_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)

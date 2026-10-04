"""
Lab partner dashboard routes.
Protected with role-based access control.
"""

from flask import Blueprint, render_template, session
from backend.data import SERVICES, AP_LOCATIONS, STATS
from backend.services import role_required

lab_bp = Blueprint('lab', __name__)


@lab_bp.route('/lab/dashboard')
@lab_bp.route('/dashboard/lab')
@role_required('lab')
def lab_dashboard():
    """Render Lab Partner Dashboard."""
    user = session.get('user')
    return render_template('dashboards/lab_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)

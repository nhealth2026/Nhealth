"""
Public page routes and basic informational APIs.
"""

from flask import Blueprint, render_template, jsonify
from backend.data import SERVICES, AP_LOCATIONS, STATS

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def home():
    """Render the main single page website."""
    return render_template('pages/index.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@pages_bp.route('/contact')
@pages_bp.route('/contact-us')
def contact_page():
    """Render the Contact Us page (Desktop and Mobile views)."""
    return render_template('pages/contact.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@pages_bp.route('/opd-dashboard')
@pages_bp.route('/membership')
@pages_bp.route('/patient/opd')
@pages_bp.route('/opd')
def opd_dashboard_page():
    """Render the Premium OPD Membership Dashboard."""
    return render_template('dashboards/opd_dashboard.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@pages_bp.route('/api/services', methods=['GET'])
def get_services():
    """Return JSON list of available services."""
    return jsonify({
        "status": "success",
        "count": len(SERVICES),
        "data": SERVICES
    })


@pages_bp.route('/api/locations', methods=['GET'])
def get_locations():
    """Return list of Andhra Pradesh coverage cities."""
    return jsonify({
        "status": "success",
        "state": "Andhra Pradesh",
        "cities": AP_LOCATIONS
    })


@pages_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Return platform statistics."""
    return jsonify({
        "status": "success",
        "data": STATS
    })

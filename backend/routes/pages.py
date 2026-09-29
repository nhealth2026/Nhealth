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


@pages_bp.route('/service/<service_slug>')
@pages_bp.route('/services/<service_slug>')
def service_detail(service_slug):
    """Render the dedicated page for a specific healthcare service."""
    service = None
    slug_lower = service_slug.strip().lower()
    
    # 1. Match by id or slug
    for s in SERVICES:
        if s.get('id', '').lower() == slug_lower or s.get('slug', '').lower() == slug_lower:
            service = s
            break
            
    # 2. Match by title slug
    if not service:
        for s in SERVICES:
            title_slug = s.get('title', '').lower().replace(' ', '-').replace('&', 'and')
            if title_slug == slug_lower or slug_lower in title_slug:
                service = s
                break
                
    # 3. Fallback to first service if not found
    if not service:
        service = SERVICES[0]
        
    related = [s for s in SERVICES if s['id'] != service['id']][:4]
    return render_template(
        'pages/service_detail.html',
        service=service,
        related_services=related,
        services=SERVICES,
        locations=AP_LOCATIONS,
        stats=STATS
    )


@pages_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Return platform statistics."""
    return jsonify({
        "status": "success",
        "data": STATS
    })

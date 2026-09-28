"""
Patient dashboard and rider booking page routes.
"""

from flask import Blueprint, render_template
from backend.data import SERVICES, AP_LOCATIONS, STATS
from backend.services import get_current_patient

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/patient/dashboard')
@patient_bp.route('/dashboard')
@patient_bp.route('/consultation')
def patient_dashboard():
    """Render the Patient Online Consultation & Healthcare Dashboard (Mobile + Laptop views)."""
    patient = get_current_patient()
    return render_template('dashboards/patient_dashboard.html', user=patient, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@patient_bp.route('/opd-dashboard')
@patient_bp.route('/membership')
@patient_bp.route('/patient/opd')
@patient_bp.route('/patient/membership')
def opd_dashboard():
    """Render the Premium OPD Membership Dashboard."""
    patient = get_current_patient()
    return render_template('dashboards/opd_dashboard.html', user=patient, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@patient_bp.route('/patient/consultation-flow')
def patient_consultation_flow():
    """Render the legacy multi-screen consultation and video calling flow."""
    patient = get_current_patient()
    return render_template('dashboards/patient_dashboard.html', user=patient, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@patient_bp.route('/rider/book')
@patient_bp.route('/book-rider')
def book_rider_page():
    """Render the dedicated Dynamic Health Support Rider Booking Page with Live Map & Route Highlighting."""
    patient = get_current_patient()
    return render_template('dashboards/book_rider.html', user=patient, locations=AP_LOCATIONS, stats=STATS)

"""
Patient dashboard and rider booking page routes.
Protected with session authentication.
"""

from flask import Blueprint, render_template
from backend.data import SERVICES, AP_LOCATIONS, STATS
from backend.services import get_current_patient, login_required

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/patient/dashboard')
@patient_bp.route('/dashboard')
@patient_bp.route('/consultation')
@login_required
def patient_dashboard():
    """Render the Patient Online Consultation & Healthcare Dashboard."""
    patient = get_current_patient()
    return render_template('dashboards/patient_dashboard.html', user=patient, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@patient_bp.route('/opd-dashboard')
@patient_bp.route('/membership')
@patient_bp.route('/patient/opd')
@patient_bp.route('/patient/membership')
@login_required
def opd_dashboard():
    """Render the Premium OPD Membership Dashboard."""
    patient = get_current_patient()
    return render_template('dashboards/opd_dashboard.html', user=patient, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@patient_bp.route('/patient/consultation-flow')
@login_required
def patient_consultation_flow():
    """Render the consultation and video calling flow."""
    patient = get_current_patient()
    return render_template('dashboards/patient_dashboard.html', user=patient, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@patient_bp.route('/rider/book')
@patient_bp.route('/book-rider')
@login_required
def book_rider_page():
    """Render the dedicated Dynamic Health Support Rider Booking Page."""
    patient = get_current_patient()
    return render_template('dashboards/book_rider.html', user=patient, locations=AP_LOCATIONS, stats=STATS)

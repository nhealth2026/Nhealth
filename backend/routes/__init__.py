"""
Routes package initialization and blueprint registration.
"""

from .pages import pages_bp
from .auth import auth_bp
from .patient import patient_bp
from .doctor import doctor_bp
from .pharmacy import pharmacy_bp
from .lab import lab_bp
from .rider import rider_bp
from .trips import trips_bp
from .bookings import bookings_bp
from .profile import profile_bp


def register_routes(app):
    """Register all application route blueprints with Flask app."""
    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(pharmacy_bp)
    app.register_blueprint(lab_bp)
    app.register_blueprint(rider_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(profile_bp)

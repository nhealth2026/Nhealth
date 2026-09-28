from .base import init_db
from .users import get_all_users, save_user, update_user
from .bookings import get_all_bookings, save_booking
from .contacts import get_all_contacts, save_contact
from .trips import (
    update_rider_duty_status, update_rider_location, create_rider_trip,
    get_trip_by_id, get_all_trips, get_available_tasks_for_riders,
    accept_trip_by_rider, update_trip_status, verify_trip_otp,
    get_rider_trip_history
)
from .invoices import generate_next_invoice_number

__all__ = [
    'init_db',
    'get_all_users', 'save_user', 'update_user',
    'get_all_bookings', 'save_booking',
    'get_all_contacts', 'save_contact',
    'update_rider_duty_status', 'update_rider_location', 'create_rider_trip',
    'get_trip_by_id', 'get_all_trips', 'get_available_tasks_for_riders',
    'accept_trip_by_rider', 'update_trip_status', 'verify_trip_otp',
    'get_rider_trip_history',
    'generate_next_invoice_number'
]

# Initialize database on module load
init_db()

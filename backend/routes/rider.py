"""
Rider dashboard and rider operational APIs.
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from backend.data import SERVICES, AP_LOCATIONS, STATS
from backend.models import (
    update_rider_duty_status,
    update_rider_location,
    get_all_trips,
    get_available_tasks_for_riders,
    accept_trip_by_rider,
    get_trip_by_id,
    update_trip_status,
    get_rider_trip_history,
    verify_trip_otp
)

rider_bp = Blueprint('rider', __name__)


@rider_bp.route('/rider/dashboard')
def rider_dashboard():
    """Render Rider Cockpit Dashboard with session authentication protection."""
    user = session.get('user')
    if not user or user.get('role') != 'rider':
        return redirect(url_for('auth.login_rider_page'))
    return render_template('dashboards/rider_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@rider_bp.route('/api/rider/status', methods=['POST'])
def api_rider_status():
    """Toggle online/offline duty status for rider."""
    data = request.get_json() or {}
    user = session.get('user')
    rider_id = data.get('rider_id') or (user.get('id') if user else 'USR-RIDER-001')
    is_online = data.get('is_online', True)
    update_rider_duty_status(rider_id, is_online)
    if user and user.get('id') == rider_id:
        session['user']['is_online'] = is_online
    return jsonify({"status": "success", "is_online": is_online})


@rider_bp.route('/api/rider/location', methods=['POST'])
def api_rider_location():
    """Update live GPS location stream from rider phone."""
    data = request.get_json() or {}
    user = session.get('user')
    rider_id = data.get('rider_id') or (user.get('id') if user else 'USR-RIDER-001')
    lat = data.get('lat', 16.5020)
    lng = data.get('lng', 80.6430)
    heading = data.get('heading', 0)
    active_trip_id = data.get('trip_id')
    update_rider_location(rider_id, lat, lng, heading, active_trip_id)
    return jsonify({"status": "success", "lat": lat, "lng": lng, "heading": heading})


@rider_bp.route('/api/rider/tasks', methods=['GET'])
def api_rider_tasks():
    """Get active trip and available dispatch task queue for rider cockpit."""
    user = session.get('user')
    rider_id = request.args.get('rider_id') or (user.get('id') if user else 'USR-RIDER-001')
    
    all_trips = get_all_trips()
    active_trip = None
    for t in all_trips:
        if t.get('rider_id') == rider_id and t.get('status') in ('accepted', 'arrived', 'in_progress', 'in_transit'):
            active_trip = t
            break
            
    available = get_available_tasks_for_riders()
    return jsonify({
        "status": "success",
        "active_trip": active_trip,
        "available_tasks": available
    })


@rider_bp.route('/api/rider/accept_task', methods=['POST'])
def api_rider_accept_task():
    """Rider accepts an incoming task."""
    data = request.get_json() or {}
    trip_id = data.get('trip_id')
    user = session.get('user') or {}
    rider_id = data.get('rider_id') or user.get('id', 'USR-RIDER-001')
    rider_name = user.get('name', 'Ravi Varma')
    rider_phone = user.get('phone', '9876543222')
    # Try to get vehicle from various fields
    rider_vehicle = (user.get('vehicle_number') or 
                     user.get('extra_data', {}).get('vehicle_number') if isinstance(user.get('extra_data'), dict) else None) or 'AP 16 CK 4589'
    # Rider current GPS position (sent from cockpit)
    rider_lat = data.get('rider_lat')
    rider_lng = data.get('rider_lng')
    
    success = accept_trip_by_rider(trip_id, rider_id, rider_name, rider_phone, rider_vehicle, rider_lat, rider_lng)
    if success:
        trip = get_trip_by_id(trip_id)
        if trip:
            return jsonify({"status": "success", "message": "Trip accepted successfully!", "trip": trip})
        return jsonify({"status": "success", "message": "Trip accepted!"})
    return jsonify({"status": "error", "message": "Failed to accept trip. It may have already been accepted."}), 400


@rider_bp.route('/api/rider/update_task_status', methods=['POST'])
def api_rider_update_task_status():
    """Update task lifecycle state (arrived, in_progress, completed, ended, cancelled)."""
    data = request.get_json() or {}
    trip_id = data.get('trip_id')
    status = data.get('status', 'arrived')
    update_trip_status(trip_id, status)
    trip = get_trip_by_id(trip_id)
    return jsonify({"status": "success", "trip": trip})


@rider_bp.route('/api/rider/history', methods=['GET'])
def api_rider_history():
    """Fetch completed, ended, and cancelled trip history for rider cockpit."""
    user = session.get('user')
    rider_id = request.args.get('rider_id') or (user.get('id') if user else None)
    if not rider_id:
        return jsonify({"status": "error", "message": "Rider authentication required."}), 401
    history = get_rider_trip_history(rider_id)
    return jsonify({
        "status": "success",
        "history": history
    })


@rider_bp.route('/api/rider/verify_otp', methods=['POST'])
def api_rider_verify_otp():
    """Verify 4-digit start OTP provided by patient."""
    data = request.get_json() or {}
    trip_id = data.get('trip_id')
    otp = data.get('otp', '').strip()
    success, msg = verify_trip_otp(trip_id, otp)
    if success:
        return jsonify({"status": "success", "message": msg, "trip": get_trip_by_id(trip_id)})
    return jsonify({"status": "error", "message": msg}), 400

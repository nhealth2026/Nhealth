"""
Trip creation, live tracking, and invoice APIs.
"""

import json
import uuid
import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from backend.models import create_rider_trip, get_trip_by_id, generate_next_invoice_number

trips_bp = Blueprint('trips', __name__)


@trips_bp.route('/api/trip/create', methods=['POST'])
def api_trip_create():
    """Create a new health support ride request from patient dashboard."""
    data = request.get_json() or {}
    trip_id = f"TRIP-{datetime.now().strftime('%y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    start_otp = str(random.randint(1000, 9999))
    invoice_num = generate_next_invoice_number("NH-INV")
    
    trip_record = {
        "trip_id": trip_id,
        "patient_name": data.get('patient_name', 'Patient').strip(),
        "patient_phone": data.get('patient_phone', '9123456780').strip(),
        "task_type": data.get('task_type', 'Patient OPD Accompaniment'),
        "pickup_address": data.get('pickup_address', 'Benz Circle, Vijayawada').strip(),
        "pickup_lat": float(data.get('pickup_lat', 16.5062)),
        "pickup_lng": float(data.get('pickup_lng', 80.6480)),
        "drop_address": data.get('drop_address', 'Ramesh Hospitals, Vijayawada').strip(),
        "drop_lat": float(data.get('drop_lat', 16.5150)),
        "drop_lng": float(data.get('drop_lng', 80.6350)),
        "rider_lat": 16.5020,
        "rider_lng": 80.6430,
        "rider_heading": 45,
        "fare_amount": int(data.get('fare_amount', 120)),
        "distance_km": float(data.get('distance_km', 2.5)),
        "start_otp": start_otp,
        "status": "searching",
        "invoice_number": invoice_num,
        "extra_data": {
            "payment_mode": "Online Only (UPI/QR)",
            "payment_status": "PAID / Online Verified",
            "payment_id": data.get('payment_id') or f"PAY-UPI-{datetime.now().strftime('%y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}",
            "invoice_number": invoice_num,
            "invoice_date": datetime.now().strftime('%d %b %Y, %I:%M %p'),
            "paid_amount": int(data.get('fare_amount', 120)),
            "cancellation_policy": "Once booked, the service cannot be cancelled or refunded.",
            "validity_policy": "The payment is valid only on that day."
        }
    }
    
    create_rider_trip(trip_record)
    
    invoice_payload = {
        "invoice_number": trip_record["invoice_number"],
        "invoice_date": trip_record["extra_data"]["invoice_date"],
        "trip_id": trip_id,
        "patient_name": trip_record['patient_name'],
        "patient_phone": trip_record['patient_phone'],
        "task_type": trip_record['task_type'],
        "pickup_address": trip_record['pickup_address'],
        "drop_address": trip_record['drop_address'],
        "fare_amount": trip_record['fare_amount'],
        "distance_km": trip_record['distance_km'],
        "payment_id": trip_record["extra_data"]["payment_id"],
        "payment_mode": trip_record["extra_data"]["payment_mode"],
        "payment_status": "PAID",
        "cancellation_policy": "Once booked, the service cannot be cancelled or refunded.",
        "validity_policy": "The payment is valid only on that day."
    }
    
    return jsonify({
        "status": "success",
        "message": "Payment verified! Health Support Rider requested. Searching for nearest rider...",
        "trip": trip_record,
        "invoice": invoice_payload
    }), 201


@trips_bp.route('/api/trip/<trip_id>/invoice', methods=['GET'])
def api_trip_invoice(trip_id):
    """Retrieve full tax invoice and receipt for a trip."""
    trip = get_trip_by_id(trip_id)
    if not trip:
        return jsonify({"status": "error", "message": "Trip not found"}), 404
    
    extra = trip.get('extra_data') or {}
    if isinstance(extra, str):
        try:
            extra = json.loads(extra)
        except Exception:
            extra = {}
            
    invoice_number = extra.get('invoice_number') or trip.get('invoice_number') or f"NH-INV-{trip_id.replace('TRIP-', '')}"
    invoice_date = extra.get('invoice_date') or datetime.now().strftime('%d %b %Y, %I:%M %p')
    payment_id = extra.get('payment_id') or f"PAY-UPI-{trip_id[:12]}"
    
    invoice = {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "trip_id": trip.get('trip_id'),
        "patient_name": trip.get('patient_name'),
        "patient_phone": trip.get('patient_phone'),
        "task_type": trip.get('task_type', 'Health Support Rider Accompaniment'),
        "pickup_address": trip.get('pickup_address'),
        "drop_address": trip.get('drop_address'),
        "fare_amount": trip.get('fare_amount', 120),
        "distance_km": trip.get('distance_km', 2.5),
        "payment_id": payment_id,
        "payment_mode": extra.get('payment_mode', 'Online Only (UPI/QR)'),
        "payment_status": "PAID",
        "cancellation_policy": "Once booked, the service cannot be cancelled or refunded.",
        "validity_policy": "The payment is valid only on that day."
    }
    return jsonify({"status": "success", "invoice": invoice})


@trips_bp.route('/api/trip/<trip_id>/live', methods=['GET'])
def api_trip_live(trip_id):
    """Retrieve real-time GPS coordinates, ETA, and status of trip."""
    trip = get_trip_by_id(trip_id)
    if not trip:
        return jsonify({"status": "error", "message": "Trip not found"}), 404
    return jsonify({
        "status": "success",
        "trip": trip
    })

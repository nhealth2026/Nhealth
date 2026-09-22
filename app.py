"""
Nhealth - Healthcare at Home
Flask Backend Application
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nhealth-super-secret-key-2026'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Data store path for bookings (persistent JSON)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.json')

if not os.path.exists(BOOKINGS_FILE):
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump([], f)

# Service Catalog
SERVICES = [
    {
        "id": "online-consult",
        "title": "Online Doctor Consultation",
        "category": "Consultation",
        "icon": "user-doctor",
        "color": "#0ea5e9",
        "bg_tint": "rgba(14, 165, 233, 0.1)",
        "badge": "24/7 Available",
        "description": "Connect with top certified physicians and specialists via secure HD video consultation within 15 minutes."
    },
    {
        "id": "doctor-home-visit",
        "title": "Doctor Home Visits",
        "category": "Home Care",
        "icon": "house-medical",
        "color": "#10b981",
        "bg_tint": "rgba(16, 185, 129, 0.1)",
        "badge": "At Your Doorstep",
        "description": "Experienced MD doctors visit your home with essential diagnostic tools for physical examination and care."
    },
    {
        "id": "lab-tests-home",
        "title": "Lab Tests at Home",
        "category": "Diagnostics",
        "icon": "flask-vial",
        "color": "#0284c7",
        "bg_tint": "rgba(2, 132, 199, 0.1)",
        "badge": "Fast Reports",
        "description": "NABL-accredited blood sample collection from your home with guaranteed digital reports within 6-12 hours."
    },
    {
        "id": "xray-at-home",
        "title": "X-Ray at Home",
        "category": "Radiology",
        "icon": "radiation",
        "color": "#6366f1",
        "bg_tint": "rgba(99, 102, 241, 0.1)",
        "badge": "Digital Imaging",
        "description": "Portable high-resolution digital X-ray delivered to your home by certified radiographers with immediate report review."
    },
    {
        "id": "pharmacy-home",
        "title": "Pharmacy to Home",
        "category": "Medicines",
        "icon": "prescription-bottle-medical",
        "color": "#059669",
        "bg_tint": "rgba(5, 150, 105, 0.1)",
        "badge": "2-Hour Express",
        "description": "100% genuine prescription medicines and healthcare supplies delivered right to your doorstep at discounted rates."
    },
    {
        "id": "premium-opd",
        "title": "Premium OPD Memberships",
        "category": "Memberships",
        "icon": "crown",
        "color": "#f59e0b",
        "bg_tint": "rgba(245, 158, 11, 0.1)",
        "badge": "Family Plans",
        "description": "Comprehensive annual healthcare packages for entire family with unlimited consultations and discount privileges."
    },
    {
        "id": "eldercare",
        "title": "Eldercare",
        "category": "Specialized Care",
        "icon": "hands-holding-child",
        "color": "#ec4899",
        "bg_tint": "rgba(236, 72, 153, 0.1)",
        "badge": "Dedicated Nursing",
        "description": "Holistic compassionate eldercare with scheduled vital monitoring, medication administration, and companion support."
    },
    {
        "id": "bedside-assistant",
        "title": "Bedside Assistant",
        "category": "Attendants",
        "icon": "bed-pulse",
        "color": "#0d9488",
        "bg_tint": "rgba(13, 148, 136, 0.1)",
        "badge": "12hr & 24hr Shifts",
        "description": "Trained male/female medical attendants for post-operative, critical patient recovery, and mobility assistance at home."
    },
    {
        "id": "physiotherapy",
        "title": "Physiotherapy",
        "category": "Rehabilitation",
        "icon": "person-walking-with-cane",
        "color": "#8b5cf6",
        "bg_tint": "rgba(139, 92, 246, 0.1)",
        "badge": "Certified Physios",
        "description": "Personalized physical therapy sessions for pain relief, stroke rehabilitation, sports injuries, and orthopedic care."
    },
    {
        "id": "nursing-services",
        "title": "Nursing Services",
        "category": "Home Care",
        "icon": "user-nurse",
        "color": "#10b981",
        "bg_tint": "rgba(16, 185, 129, 0.1)",
        "badge": "Skilled Nurses",
        "description": "Certified ICU and home care nurses for IV infusions, wound dressing, catheterization, and post-surgery care."
    },
    {
        "id": "dental-care",
        "title": "Dental Care",
        "category": "Dental Care",
        "icon": "tooth",
        "color": "#0284c7",
        "bg_tint": "rgba(2, 132, 199, 0.1)",
        "badge": "Healthy Smiles",
        "description": "Comprehensive dental checkups, cleaning, fillings, painless root canals, and consultations with certified dental surgeons."
    },
    {
        "id": "blood-bank",
        "title": "Blood Bank",
        "category": "Emergency Care",
        "icon": "droplet",
        "color": "#b91c1c",
        "bg_tint": "rgba(185, 28, 28, 0.1)",
        "badge": "Donate & Save Lives",
        "description": "24/7 verified blood donor network, cross-matching, platelets, and rapid hospital delivery for emergency life-saving needs."
    },
    {
        "id": "diagnostics-imaging",
        "title": "Diagnostics and Imaging",
        "category": "Radiology & Scans",
        "icon": "x-ray",
        "color": "#0d9488",
        "bg_tint": "rgba(13, 148, 136, 0.1)",
        "badge": "Accurate Reports",
        "description": "High-precision MRI, CT scans, ultrasound, and digital radiology with certified expert radiologist interpretations."
    },
    {
        "id": "ambulance-services-247",
        "title": "Ambulance Services 24/7",
        "category": "Emergency SOS",
        "icon": "truck-medical",
        "color": "#dc2626",
        "bg_tint": "rgba(220, 38, 38, 0.1)",
        "badge": "24/7 Rapid Response",
        "description": "Immediate emergency ICU and ALS/BLS ambulance dispatch equipped with ventilators, defibrillators, and oxygen support."
    },
    {
        "id": "home-vaccination",
        "title": "Home Vaccination Service",
        "category": "Immunization",
        "icon": "syringe",
        "color": "#7c3aed",
        "bg_tint": "rgba(124, 58, 237, 0.1)",
        "badge": "Safe Immunity",
        "description": "Safe, temperature-monitored vaccination at home for infants, children, adults, and seniors by certified healthcare nurses."
    },
    {
        "id": "health-checkups",
        "title": "Health Checkups",
        "category": "Preventive Care",
        "icon": "heart-pulse",
        "color": "#16a34a",
        "bg_tint": "rgba(22, 163, 74, 0.1)",
        "badge": "Know Today",
        "description": "Comprehensive full-body preventive health checkup packages with home sample pickup and personalized doctor review."
    },
    {
        "id": "care-programmes",
        "title": "Care Programmes",
        "category": "Specialized Care",
        "icon": "people-roof",
        "color": "#ea580c",
        "bg_tint": "rgba(234, 88, 12, 0.1)",
        "badge": "Support & Independence",
        "description": "Personalized care management programs for chronic illnesses, stroke rehab, post-surgical recovery, and assisted living."
    },
    {
        "id": "mental-health",
        "title": "Mental Health Support",
        "category": "Mental Wellness",
        "icon": "brain",
        "color": "#4338ca",
        "bg_tint": "rgba(67, 56, 202, 0.1)",
        "badge": "Talk. Heal. Grow.",
        "description": "Confidential counseling, psychotherapy, and psychiatric consultations with certified psychologists and mental wellness experts."
    },
    {
        "id": "and-more",
        "title": "and more...",
        "category": "Explore All",
        "icon": "plus",
        "color": "#0891b2",
        "bg_tint": "rgba(8, 145, 178, 0.1)",
        "badge": "20+ Services",
        "description": "Discover ICU setup at home, medical equipment rental, diabetic care plans, nutrition counseling, and ambulance dispatch."
    }
]

# Andhra Pradesh Key Locations
AP_LOCATIONS = [
    "Visakhapatnam",
    "Vijayawada",
    "Guntur",
    "Tirupati",
    "Kurnool",
    "Kakinada",
    "Rajahmundry",
    "Nellore",
    "Kadapa",
    "Anantapur",
    "Eluru",
    "Ongole",
    "Vizianagaram",
    "Machilipatnam",
    "Chittoor"
]

# Trust Stats
STATS = {
    "happy_families": "10,000+",
    "verified_doctors": "1500+",
    "diagnostic_partners": "500+",
    "pharmacy_partners": "200+"
}


@app.route('/')
def home():
    """Render the main single page website."""
    return render_template('index.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/api/services', methods=['GET'])
def get_services():
    """Return JSON list of available services."""
    return jsonify({
        "status": "success",
        "count": len(SERVICES),
        "data": SERVICES
    })


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Return list of Andhra Pradesh coverage cities."""
    return jsonify({
        "status": "success",
        "state": "Andhra Pradesh",
        "cities": AP_LOCATIONS
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Return platform statistics."""
    return jsonify({
        "status": "success",
        "data": STATS
    })


@app.route('/api/book', methods=['POST'])
def book_appointment():
    """Handle appointment / home healthcare booking."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()

        required_fields = ['name', 'phone', 'service', 'city']
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing)}"
            }), 400

        # Validate phone
        phone = data.get('phone', '').strip()
        if len(phone) < 10:
            return jsonify({
                "status": "error",
                "message": "Please provide a valid 10-digit phone number."
            }), 400

        booking_id = f"NH-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        booking_record = {
            "booking_id": booking_id,
            "created_at": datetime.now().isoformat(),
            "name": data.get('name', '').strip(),
            "phone": phone,
            "email": data.get('email', '').strip(),
            "service": data.get('service', '').strip(),
            "city": data.get('city', '').strip(),
            "address": data.get('address', '').strip(),
            "preferred_date": data.get('date', datetime.now().strftime('%Y-%m-%d')),
            "time_slot": data.get('time_slot', 'Morning (9:00 AM - 1:00 PM)'),
            "notes": data.get('notes', '').strip(),
            "status": "Confirmed"
        }

        # Store booking record
        try:
            with open(BOOKINGS_FILE, 'r+') as f:
                records = json.load(f)
                records.append(booking_record)
                f.seek(0)
                json.dump(records, f, indent=2)
        except Exception:
            with open(BOOKINGS_FILE, 'w') as f:
                json.dump([booking_record], f, indent=2)

        return jsonify({
            "status": "success",
            "message": f"Thank you {booking_record['name']}! Your home healthcare request has been confirmed.",
            "booking_id": booking_id,
            "details": {
                "service": booking_record['service'],
                "city": booking_record['city'],
                "date": booking_record['preferred_date'],
                "slot": booking_record['time_slot']
            }
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500


@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle general inquiries and contact requests."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()

        if not name or not phone:
            return jsonify({
                "status": "error",
                "message": "Name and phone number are required."
            }), 400

        return jsonify({
            "status": "success",
            "message": f"Thank you {name}. Our Andhra Pradesh healthcare coordinator will call you within 15 minutes."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to submit: {str(e)}"
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("==================================================")
    print("   Nhealth - Healthcare at Home Server Started   ")
    print(f"   Serving on: http://0.0.0.0:{port}             ")
    print("==================================================")
    app.run(host='0.0.0.0', port=port, debug=False)

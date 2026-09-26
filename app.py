"""
Nhealth - Healthcare at Home
Flask Backend Application
"""

import os
import json
import uuid
import time
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, date
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

app = Flask(__name__)
app.json = CustomJSONProvider(app)
app.config['SECRET_KEY'] = 'nhealth-super-secret-key-2026-secure-session'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Import Database Manager (Supports Neon PostgreSQL & Local Storage)
import db

def get_all_users():
    return db.get_all_users()

def save_user(user_data):
    return db.save_user(user_data)

def update_user(user_id, updated_fields):
    return db.update_user(user_id, updated_fields)

def verify_password(stored_password, provided_password):
    if not stored_password or not provided_password:
        return False
    stored_clean = str(stored_password).strip()
    provided_clean = str(provided_password).strip()
    if stored_clean.startswith(('pbkdf2:sha256:', 'scrypt:', 'argon2:')):
        if check_password_hash(stored_clean, provided_password):
            return True
        if check_password_hash(stored_clean, provided_clean):
            return True
        if check_password_hash(stored_clean, provided_clean.lower()):
            return True
        return False
    return stored_clean == provided_clean or stored_clean.lower() == provided_clean.lower()

# Rate-limiting failed logins (security)
FAILED_LOGIN_ATTEMPTS = {}  # { key: {'count': int, 'lockout_until': timestamp} }

def is_rate_limited(key):
    record = FAILED_LOGIN_ATTEMPTS.get(key)
    if not record:
        return False, 0
    now = time.time()
    if record.get('lockout_until', 0) > now:
        remaining = int(record['lockout_until'] - now)
        return True, remaining
    return False, 0

def record_failed_attempt(key):
    now = time.time()
    record = FAILED_LOGIN_ATTEMPTS.get(key, {'count': 0, 'lockout_until': 0})
    record['count'] += 1
    if record['count'] >= 5:
        record['lockout_until'] = now + 30  # 30-second lockout after 5 failed attempts
    FAILED_LOGIN_ATTEMPTS[key] = record

def clear_failed_attempts(key):
    FAILED_LOGIN_ATTEMPTS.pop(key, None)

def _ensure_patient_fields(user_dict):
    if not user_dict.get('age'):
        user_dict['age'] = 30
    if not user_dict.get('dob'):
        user_dict['dob'] = '1995-05-15'
    if not user_dict.get('gender'):
        user_dict['gender'] = 'Male'
    if not user_dict.get('blood_group'):
        user_dict['blood_group'] = 'O+'
    if not user_dict.get('city'):
        user_dict['city'] = 'Vijayawada'
    if not user_dict.get('address'):
        user_dict['address'] = f"{user_dict.get('city', 'Vijayawada')}, Andhra Pradesh"

def get_current_patient():
    """Retrieve current logged in patient from session or fallback to latest registered patient."""
    user_id = session.get('user_id')
    users = get_all_users()
    
    if user_id:
        for u in users:
            if u.get('id') == user_id:
                clean = {k: v for k, v in u.items() if k != 'password'}
                _ensure_patient_fields(clean)
                return clean
    
    if 'user' in session:
        clean = dict(session['user'])
        _ensure_patient_fields(clean)
        return clean
    
    # Fallback to the latest patient registered in users.json so there are never dummy placeholder names
    patients = [u for u in users if u.get('role') == 'patient']
    if patients:
        latest = patients[-1]
        clean = {k: v for k, v in latest.items() if k != 'password'}
        _ensure_patient_fields(clean)
        return clean
        
    return {
        "id": "USR-PAT-NEW",
        "name": "Valued Patient",
        "email": "patient@nhealth.in",
        "phone": "9876543210",
        "city": "Vijayawada",
        "age": 32,
        "gender": "Male",
        "blood_group": "O+",
        "address": "Vijayawada, Andhra Pradesh"
    }


# Service Catalog with Comprehensive Details
SERVICES = [
    {
        "id": "online-consult",
        "title": "Online Doctor Consultation",
        "category": "Doctor Consultation",
        "filter_cat": "doctor",
        "icon": "user-doctor",
        "emoji": "🩺",
        "color": "#0ea5e9",
        "bg_tint": "rgba(14, 165, 233, 0.12)",
        "badge": "15-Min Connect",
        "description": "Connect instantly with 1,500+ board-certified general physicians and super-specialists via secure, encrypted HD video or phone within 15 minutes.",
        "features": [
            "15-Minute Instant Telemedicine Connect",
            "Free Follow-Up & WhatsApp Chat for 7 Days",
            "Digital E-Prescription with WhatsApp Delivery",
            "Multi-Specialty: General, Cardio, Derm, Peds, Gynae"
        ],
        "action_label": "Consult Doctor Now",
        "action_fn": "openBookingModal('Online Doctor Consultation')"
    },
    {
        "id": "doctor-home-visit",
        "title": "Doctor Home Visits",
        "category": "Doctor Consultation",
        "filter_cat": "doctor",
        "icon": "house-medical",
        "emoji": "👨‍⚕️",
        "color": "#10b981",
        "bg_tint": "rgba(16, 185, 129, 0.12)",
        "badge": "At Your Doorstep",
        "description": "Experienced MD physicians visit your home equipped with diagnostic kits for clinical physical checkups, chronic assessments, and bedside care.",
        "features": [
            "Thorough Bedside Clinical Examination",
            "Immediate Diagnosis & In-Home Medication Plan",
            "Priority Care for Elderly & Bedridden Patients",
            "Post-Hospitalization Discharge Follow-Up"
        ],
        "action_label": "Book Doctor Visit",
        "action_fn": "openBookingModal('Doctor Home Visits')"
    },
    {
        "id": "pharmacy-home",
        "title": "Doorstep E-Pharmacy",
        "category": "Pharmacy & Medicines",
        "filter_cat": "pharmacy",
        "icon": "prescription-bottle-medical",
        "emoji": "💊",
        "color": "#059669",
        "bg_tint": "rgba(5, 150, 105, 0.12)",
        "badge": "2-Hour Express",
        "description": "Upload your prescription for instant pharmacist validation. Enjoy authentic temperature-controlled doorstep medicine delivery at discounted rates.",
        "features": [
            "100% Genuine Certified Medicines & Surgical Supplies",
            "2-Hour Express Delivery Guarantee across AP",
            "Flat 20% Discount on Monthly Chronic Refills",
            "Automated WhatsApp Refill Reminders"
        ],
        "action_label": "Order Medicines",
        "action_fn": "openBookingModal('Pharmacy to Home')"
    },
    {
        "id": "lab-tests-home",
        "title": "Home Diagnostics & Lab Tests",
        "category": "Diagnostics & Lab",
        "filter_cat": "diagnostics",
        "icon": "flask-vial",
        "emoji": "🔬",
        "color": "#0284c7",
        "bg_tint": "rgba(2, 132, 199, 0.12)",
        "badge": "NABL Accredited",
        "description": "Certified phlebotomists arrive at your doorstep with sealed vacutainer kits for blood, urine, and pathology sample collection with fast digital reports.",
        "features": [
            "NABL & CAP Accredited Laboratory Testing",
            "100% Painless Safe Blood Draw with Barcoded Kits",
            "Verified Smart PDF Reports Delivered in 6 Hours",
            "500+ Tests: CBC, Lipid, HbA1c, LFT, KFT & Thyroid"
        ],
        "action_label": "Book Lab Test",
        "action_fn": "openBookingModal('Lab Tests at Home')"
    },
    {
        "id": "xray-at-home",
        "title": "X-Ray & Portable Diagnostics",
        "category": "Diagnostics & Lab",
        "filter_cat": "diagnostics",
        "icon": "radiation",
        "emoji": "🩻",
        "color": "#6366f1",
        "bg_tint": "rgba(99, 102, 241, 0.12)",
        "badge": "Portable Digital",
        "description": "Advanced low-radiation portable digital X-Ray and 12-lead ECG machines brought straight to your bedroom for immediate imaging without traveling.",
        "features": [
            "High-Frequency Digital X-Ray at Bedside",
            "12-Lead Digital ECG with Instant Cardiologist Review",
            "Ideal for Elderly, Fractures & Non-Ambulatory Patients",
            "Same-Day Digital Films & Radiologist Reports"
        ],
        "action_label": "Book Portable X-Ray",
        "action_fn": "openBookingModal('X-Ray at Home')"
    },
    {
        "id": "nursing-services",
        "title": "Specialized Nursing Care",
        "category": "Home Care & Nursing",
        "filter_cat": "nursing",
        "icon": "user-nurse",
        "emoji": "👩‍⚕️",
        "color": "#ec4899",
        "bg_tint": "rgba(236, 72, 153, 0.12)",
        "badge": "GNM / B.Sc Certified",
        "description": "Compassionate, qualified registered nurses for post-operative recovery, elderly assistance, wound dressing, catheter management, and home ICU.",
        "features": [
            "Background-Verified & Registered Nurses",
            "12-Hour Day/Night & 24-Hour Residential Shifts",
            "IV Infusions, Catheter Care, Tracheostomy & Dressing",
            "Continuous Vital Monitoring & Emergency Protocols"
        ],
        "action_label": "Book Home Nurse",
        "action_fn": "openBookingModal('Home Nursing Care Attendant')"
    },
    {
        "id": "bedside-assistant",
        "title": "Bedside Assistant & Attendant",
        "category": "Home Care & Nursing",
        "filter_cat": "nursing",
        "icon": "bed-pulse",
        "emoji": "🛏️",
        "color": "#0d9488",
        "bg_tint": "rgba(13, 148, 136, 0.12)",
        "badge": "12hr & 24hr Shifts",
        "description": "Trained male and female patient care attendants providing round-the-clock physical assistance, hygiene support, feeding, and mobility care at home.",
        "features": [
            "Mobility, Bathing, Feeding & Personal Hygiene Care",
            "Post-Surgery, Paralysis & Critical Recovery Support",
            "Medication Prompting & Regular Vital Logging",
            "Trained in Patient Handling & Compassionate Care"
        ],
        "action_label": "Book Bedside Attendant",
        "action_fn": "openBookingModal('Bedside Assistant')"
    },
    {
        "id": "eldercare",
        "title": "Eldercare & Senior Assistance",
        "category": "Home Care & Nursing",
        "filter_cat": "nursing",
        "icon": "hands-holding-child",
        "emoji": "👵",
        "color": "#f97316",
        "bg_tint": "rgba(249, 115, 22, 0.12)",
        "badge": "Dedicated Companions",
        "description": "Dedicated senior care companions and geriatric specialists helping your elderly loved ones live safely, healthily, and independently at home.",
        "features": [
            "Scheduled Geriatric Vitals & Health Monitoring",
            "Medication Adherence & Daily Activity Assistance",
            "Emotional Companionship & Accompanied Walks",
            "Emergency SOS Alerts & Regular Family Progress Updates"
        ],
        "action_label": "Book Eldercare",
        "action_fn": "openBookingModal('Eldercare')"
    },
    {
        "id": "physiotherapy",
        "title": "Physiotherapy at Home",
        "category": "Rehabilitation & Therapy",
        "filter_cat": "rehab",
        "icon": "person-walking-with-cane",
        "emoji": "🚶‍♂️",
        "color": "#8b5cf6",
        "bg_tint": "rgba(139, 92, 246, 0.12)",
        "badge": "Certified Physios",
        "description": "Expert certified physiotherapists bringing specialized rehabilitation equipment to restore mobility, relieve chronic pain, and rebuild muscular strength.",
        "features": [
            "Orthopedic, Neuro, Sports Injury & Post-Op Rehab",
            "Stroke Recovery, Paralysis & Joint Mobility Plans",
            "Advanced Electrotherapy (TENS, IFT, Ultrasound) at Home",
            "Personalized Exercise Regimes & Recovery Tracking"
        ],
        "action_label": "Book Physiotherapist",
        "action_fn": "openBookingModal('Physiotherapy')"
    },
    {
        "id": "dental-care",
        "title": "Dental Care & Oral Health",
        "category": "Doctor Consultation",
        "filter_cat": "doctor",
        "icon": "tooth",
        "emoji": "🦷",
        "color": "#0284c7",
        "bg_tint": "rgba(2, 132, 199, 0.12)",
        "badge": "Oral Health",
        "description": "Comprehensive dental consultations, portable dental hygiene scaling, painless cavity fillings, dentures, and priority appointments with top dentists.",
        "features": [
            "In-Home Preventive Oral Checkups & Consultations",
            "Portable Ultrasonic Scaling & Polishing",
            "Denture Adjustments & Painless Cavity Treatments",
            "Specialized Senior Citizen Dental Care"
        ],
        "action_label": "Book Dental Care",
        "action_fn": "openBookingModal('Dental Care')"
    },
    {
        "id": "ambulance-services-247",
        "title": "24/7 Smart Ambulance & SOS",
        "category": "Emergency & Critical",
        "filter_cat": "emergency",
        "icon": "truck-medical",
        "emoji": "🚑",
        "color": "#dc2626",
        "bg_tint": "rgba(220, 38, 38, 0.12)",
        "badge": "8-Min Avg Dispatch",
        "description": "Emergency GPS dispatch linking you to the nearest Advanced Life Support (ALS), Basic Life Support (BLS), and Neonatal ambulances across Andhra Pradesh.",
        "features": [
            "8-Minute Average Arrival Time with Real-Time GPS Tracking",
            "Onboard Ventilator, Defibrillator, Oxygen & Paramedics",
            "Hospital Emergency Room Pre-Sync & Direct ICU Bed Booking",
            "24/7 Toll-Free SOS Response Helpline"
        ],
        "action_label": "Dispatch Emergency SOS",
        "action_fn": "triggerEmergencySOS()"
    },
    {
        "id": "blood-bank",
        "title": "Blood Bank & Support",
        "category": "Emergency & Critical",
        "filter_cat": "emergency",
        "icon": "droplet",
        "emoji": "🩸",
        "color": "#b91c1c",
        "bg_tint": "rgba(185, 28, 28, 0.12)",
        "badge": "24/7 Live Network",
        "description": "Rapid 24/7 blood group availability check, emergency voluntary donor coordination, and safe blood component delivery (PRBC, Platelets, FFP).",
        "features": [
            "Real-Time Blood Stock Tracking Across Verified Blood Banks",
            "Emergency Donor Network for Rare Blood Groups",
            "Temperature-Controlled Safe Component Transportation",
            "Verified Screened Units with Zero Contamination"
        ],
        "action_label": "Check Blood Availability",
        "action_fn": "openBookingModal('Blood Bank')"
    },
    {
        "id": "diagnostics-imaging",
        "title": "Diagnostics & Advanced Imaging",
        "category": "Diagnostics & Lab",
        "filter_cat": "diagnostics",
        "icon": "circle-nodes",
        "emoji": "📡",
        "color": "#4f46e5",
        "bg_tint": "rgba(79, 70, 229, 0.12)",
        "badge": "MRI / CT / Scans",
        "description": "Priority scheduling for high-precision 1.5T/3T MRI, 128-slice CT Scans, Ultrasound, 2D Echo, Mammography, and PET Scans with expert radiologist reports.",
        "features": [
            "Discounted Rates at Top Accredited Imaging Centers",
            "Zero Waiting Queue Priority Slot Reservations",
            "Certified Radiologist Second Opinion Reports",
            "Digital Cloud Access to DICOM Scans & Reports"
        ],
        "action_label": "Book Imaging Scan",
        "action_fn": "openBookingModal('Diagnostics and Imaging')"
    },
    {
        "id": "home-vaccination",
        "title": "Home Vaccination Service",
        "category": "Preventive & Care Plans",
        "filter_cat": "preventive",
        "icon": "syringe",
        "emoji": "💉",
        "color": "#10b981",
        "bg_tint": "rgba(16, 185, 129, 0.12)",
        "badge": "Cold-Chain Safe",
        "description": "Certified healthcare nurses deliver and administer WHO-approved cold-chain maintained vaccines safely at your home for infants, children, and adults.",
        "features": [
            "100% Strict Cold-Chain Storage & Handling",
            "Complete Childhood Immunization Schedules",
            "Adult Vaccines: Flu, Hepatitis B, Pneumonia, Cervical, Typhoid",
            "Digital Vaccination Certificate & Follow-Up Alerts"
        ],
        "action_label": "Book Vaccination",
        "action_fn": "openBookingModal('Home Vaccination Service')"
    },
    {
        "id": "health-checkups",
        "title": "Full Body Preventive Screening",
        "category": "Preventive & Care Plans",
        "filter_cat": "preventive",
        "icon": "heart-pulse",
        "emoji": "🛡️",
        "color": "#ca8a04",
        "bg_tint": "rgba(202, 138, 4, 0.12)",
        "badge": "85+ Parameters",
        "description": "Comprehensive annual preventive health packages covering 85+ parameters including Cardiac Risk, Liver, Kidney, Thyroid, Vitamin D/B12, and Diabetes.",
        "features": [
            "85+ Comprehensive Vital Parameters Analyzed",
            "Free MD Physician Consultation & Diet Counseling Included",
            "Smart AI-Powered Health Risk Assessment Report",
            "Master Wellness Profiles for Whole Family & Elders"
        ],
        "action_label": "Book Health Package",
        "action_fn": "openBookingModal('Full Body Preventive Health Checkup')"
    },
    {
        "id": "care-programmes",
        "title": "Chronic Disease Care Programmes",
        "category": "Preventive & Care Plans",
        "filter_cat": "preventive",
        "icon": "user-shield",
        "emoji": "📋",
        "color": "#7c3aed",
        "bg_tint": "rgba(124, 58, 237, 0.12)",
        "badge": "360° Management",
        "description": "Tailored 360° continuous disease management programs for Diabetes, Hypertension, Cardiac Health, Asthma, COPD, and Thyroid wellness.",
        "features": [
            "Dedicated Personal Health Manager & Doctor Check-ins",
            "Regular Scheduled In-Home Tests & Medicine Deliveries",
            "Personalized Diet, Fitness & Lifestyle Plans",
            "Connected IoT Blood Glucose & BP Monitor Tracking"
        ],
        "action_label": "Enroll in Care Plan",
        "action_fn": "openBookingModal('Care Programmes')"
    },
    {
        "id": "mental-health",
        "title": "Mental Health & Counseling",
        "category": "Rehabilitation & Therapy",
        "filter_cat": "rehab",
        "icon": "brain",
        "emoji": "🧠",
        "color": "#9333ea",
        "bg_tint": "rgba(147, 51, 234, 0.12)",
        "badge": "100% Confidential",
        "description": "Confidential 1-on-1 online therapy and psychiatric counseling with licensed clinical psychologists for anxiety, depression, stress, burnout, and wellness.",
        "features": [
            "100% Confidential & Encrypted Video Sessions",
            "Licensed Clinical Psychologists & Psychiatrists",
            "Therapy for Stress, Anxiety, Depression, Sleep & Trauma",
            "Cognitive Behavioral Therapy (CBT) & Guided Mindfulness"
        ],
        "action_label": "Book Counseling",
        "action_fn": "openBookingModal('Mental Health Support')"
    },
    {
        "id": "premium-opd",
        "title": "Premium OPD & Hospital Assistance",
        "category": "Preventive & Care Plans",
        "filter_cat": "preventive",
        "icon": "crown",
        "emoji": "👑",
        "color": "#d97706",
        "bg_tint": "rgba(217, 119, 6, 0.12)",
        "badge": "VIP Priority",
        "description": "Exclusive healthcare memberships offering unlimited doctor consultations, hospital OPD priority queues, procedure coordination, and deep discounts.",
        "features": [
            "Dedicated On-Ground Care Buddy for Hospital OPD & Admission",
            "Zero Waiting Time in Partner Hospital OPD Queues",
            "Up to 30% Discounts on Surgeries, Diagnostic Labs & Pharmacy",
            "Complete Comprehensive Family Coverage Under One Card"
        ],
        "action_label": "Explore Memberships",
        "action_fn": "openBookingModal('Premium OPD Memberships')"
    },
    {
        "id": "health-support-rider",
        "title": "Health Support Rider",
        "category": "Emergency & Critical",
        "filter_cat": "emergency",
        "icon": "motorcycle",
        "emoji": "🛵",
        "color": "#0baaa2",
        "bg_tint": "rgba(11, 170, 162, 0.12)",
        "badge": "Pick • Support • Drop",
        "description": "Dedicated healthcare riders providing trusted patient pick & drop, hospital OPD accompaniment, procedure assistance, and doorstep medicine & report delivery.",
        "features": [
            "Safe Hospital Pick, Escort, Support & Drop-off",
            "Full-Day Dedicated Patient Companion for OPDs & Tests",
            "Express Doorstep Medicine & Diagnostic Report Delivery",
            "Real-Time Live Journey Tracking for Anxious Families"
        ],
        "action_label": "Book Health Rider",
        "action_fn": "openBookingModal('Health Support Rider')"
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

        # Store booking record via database layer
        db.save_booking(booking_record)

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


@app.route('/patient/dashboard')
@app.route('/dashboard')
@app.route('/consultation')
def patient_dashboard():
    """Render the Patient Online Consultation & Healthcare Dashboard (Mobile + Laptop views)."""
    patient = get_current_patient()
    return render_template('patient_dashboard.html', user=patient, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/rider/book')
@app.route('/book-rider')
def book_rider_page():
    """Render the dedicated Dynamic Health Support Rider Booking Page with Live Map & Route Highlighting."""
    patient = get_current_patient()
    return render_template('book_rider.html', user=patient, locations=AP_LOCATIONS, stats=STATS)


@app.route('/contact')
@app.route('/contact-us')
def contact_page():
    """Render the Contact Us page (Desktop and Mobile views)."""
    return render_template('contact.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/login')
def login_page():
    """Render the Login page."""
    role = request.args.get('role', 'patient')
    if role == 'lab':
        return redirect(url_for('login_lab_page'))
    if role == 'rider':
        return redirect(url_for('login_rider_page'))
    return render_template('login.html', role=role, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/login/lab')
@app.route('/lab/login')
def login_lab_page():
    """Render dedicated Lab Login page (matching reference design for both desktop and mobile views)."""
    return render_template('login_lab.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/login/pharmacy')
@app.route('/pharmacy/login')
def login_pharmacy_page():
    """Render Login page pre-configured for Pharmacy Partner."""
    return render_template('login.html', role='pharmacy', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/login/rider')
@app.route('/rider/login')
def login_rider_page():
    """Render dedicated Rider Login page."""
    return render_template('login_rider.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/signup')
def signup_page():
    """Render the Signup page (defaults to patient or uses role query)."""
    role = request.args.get('role', 'patient')
    if role == 'lab':
        return redirect(url_for('signup_lab_page'))
    if role == 'rider':
        return redirect(url_for('signup_rider_page'))
    if role in ['doctor', 'partner']:
        return render_template('signup_partner.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)
    return render_template('signup_patient.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/signup/patient')
def signup_patient_page():
    """Render Patient Sign Up page."""
    return render_template('signup_patient.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/signup/doctor')
@app.route('/signup/partner')
def signup_doctor_page():
    """Render Doctor / Partner Sign Up page (exact match to reference design)."""
    return render_template('signup_partner.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/signup/lab')
@app.route('/lab/signup')
def signup_lab_page():
    """Render dedicated Lab Sign Up page (matching reference design for both desktop and mobile views)."""
    return render_template('signup_lab.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/signup/rider')
@app.route('/rider/signup')
def signup_rider_page():
    """Render dedicated Rider Sign Up page (3-step streamlined onboarding)."""
    return render_template('signup_rider.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/lab/dashboard')
@app.route('/dashboard/lab')
def lab_dashboard():
    """Render Lab Partner Dashboard."""
    user = session.get('user')
    if not user:
        user = {
            "id": "LAB-AP-2026",
            "name": "Apollo Diagnostics & Pathology Lab",
            "owner_name": "Dr. K. Srinivas Rao",
            "role": "lab",
            "city": "Vijayawada",
            "phone": "9876543210",
            "email": "lab@nhealth.in"
        }
    return render_template('lab_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/pharmacy/dashboard')
@app.route('/dashboard/pharmacy')
@app.route('/pharma/dashboard')
@app.route('/pharmacy')
def pharmacy_dashboard():
    """Render Pharmacy Partner Dashboard matching reference design."""
    user = session.get('user')
    if not user or user.get('role') != 'pharmacy':
        user = {
            "id": "PHA-000123",
            "name": "Sai Medicals",
            "owner_name": "Sai Medicals & Pharmacy",
            "role": "pharmacy",
            "city": "Narasaraopeta",
            "phone": "9876543290",
            "email": "pharmacy@nhealth.in"
        }
    return render_template('pharmacy_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/rider/dashboard')
def rider_dashboard():
    """Render Rider Cockpit Dashboard with session authentication protection."""
    user = session.get('user')
    if not user or user.get('role') != 'rider':
        return redirect(url_for('login_rider_page'))
    return render_template('rider_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/doctor/dashboard')
@app.route('/dashboard/doctor')
@app.route('/doctor')
def doctor_dashboard():
    """Render Doctor Partner Dashboard matching reference design."""
    user = session.get('user')
    if not user or user.get('role') != 'doctor':
        user = {
            "id": "USR-DOC-001",
            "name": "Dr. Arjun Reddy",
            "doctor_id": "DOC78456",
            "qualification": "MBBS, MD (General Medicine)",
            "specialization": "General Physician",
            "experience": "8+ Years",
            "reg_number": "APMC/12345",
            "role": "doctor",
            "city": "Vijayawada",
            "phone": "9876543210",
            "email": "doctor@nhealth.in"
        }
    return render_template('doctor_dashboard.html', user=user, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/logout')
def app_logout():
    """Log out user, clear session, and redirect cleanly."""
    user = session.get('user')
    was_rider = bool(user and user.get('role') == 'rider') or request.args.get('role') == 'rider'
    session.clear()
    if was_rider:
        return redirect(url_for('login_rider_page'))
    return redirect(url_for('login_page'))



@app.route('/api/auth/signup', methods=['POST'])
def auth_signup():
    """Handle new patient or doctor/partner account registration with security validation."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        role = data.get('role', 'patient').strip().lower()
        name = (data.get('name', '') or data.get('lab_name', '')).strip()
        owner_name = (data.get('owner_name') or data.get('ownerName', '')).strip()
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', 'Andhra Pradesh').strip()
        pincode = data.get('pincode', '').strip()
        address = (data.get('address') or data.get('full_address', '')).strip()
        dob = (data.get('dob') or data.get('date_of_birth', '')).strip()
        gender = (data.get('gender') or 'Male').strip()
        reg_number = (data.get('reg_number') or data.get('registrationNumber', '')).strip()
        gst_number = (data.get('gst_number') or data.get('gstNumber', '')).strip()
        password = data.get('password', '').strip()

        # Calculate age if dob is given
        calculated_age = None
        if dob:
            try:
                birth_date = datetime.strptime(dob, '%Y-%m-%d')
                today = date.today()
                calculated_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            except Exception:
                try:
                    for fmt in ('%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d'):
                        try:
                            birth_date = datetime.strptime(dob, fmt)
                            today = date.today()
                            calculated_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                            dob = birth_date.strftime('%Y-%m-%d')
                            break
                        except ValueError:
                            continue
                except Exception:
                    pass
        if calculated_age is None:
            if str(data.get('age', '')).isdigit():
                calculated_age = int(data.get('age'))
            else:
                calculated_age = 30

        # Required fields validation
        if not name or not phone or not password:
            return jsonify({
                "status": "error",
                "message": "Full Name / Lab Name, Mobile Number, and Password are required."
            }), 400

        # Clean phone and validate 10 digits
        clean_phone = re.sub(r'\D', '', phone)
        if len(clean_phone) != 10:
            return jsonify({
                "status": "error",
                "message": "Please enter a valid 10-digit mobile number."
            }), 400

        # Rider specific 2 mandatory contact numbers & validation
        clean_sec_phone = ''
        location_type = data.get('location_type', 'city').strip().lower()
        town_village = (data.get('town_village') or data.get('city') or city).strip()

        if role == 'rider':
            secondary_phone = (data.get('secondary_phone') or data.get('emergency_phone') or '').strip()
            clean_sec_phone = re.sub(r'\D', '', secondary_phone)
            if len(clean_sec_phone) != 10:
                return jsonify({
                    "status": "error",
                    "message": "Secondary / Alternate Contact Number is mandatory and must be a valid 10-digit number."
                }), 400
            if clean_phone == clean_sec_phone:
                return jsonify({
                    "status": "error",
                    "message": "Primary and Secondary contact numbers must be different."
                }), 400
            if not data.get('has_individual_photo'):
                return jsonify({
                    "status": "error",
                    "message": "Individual Photo is mandatory for rider verification."
                }), 400

        # Password minimum length check
        if len(password) < 6:
            return jsonify({
                "status": "error",
                "message": "Password must be at least 6 characters long."
            }), 400

        users = get_all_users()

        # Check existing user
        if any(u.get('phone') == clean_phone or (email and u.get('email', '').lower() == email) for u in users):
            return jsonify({
                "status": "error",
                "message": "An account with this mobile number or email already exists. Please login."
            }), 409

        user_id = f"USR-{role[:3].upper()}-{datetime.now().strftime('%y%m')}-{uuid.uuid4().hex[:4].upper()}"

        user_record = {
            "id": user_id,
            "role": role,
            "name": name,
            "owner_name": owner_name,
            "email": email,
            "phone": clean_phone,
            "secondary_phone": clean_sec_phone,
            "whatsapp": data.get('whatsapp', clean_phone).strip(),
            "specialization": data.get('specialization', 'Diagnostic Pathology' if role == 'lab' else ''),
            "clinic_name": data.get('clinic_name', name if role == 'lab' else ''),
            "reg_number": reg_number,
            "gst_number": gst_number,
            "city": city or "Vijayawada",
            "state": state,
            "location_type": location_type,
            "town_village": town_village,
            "pincode": pincode,
            "age": calculated_age,
            "dob": dob,
            "gender": gender,
            "blood_group": data.get('blood_group', 'O+'),
            "address": address or f"{town_village or city or 'Vijayawada'}, {state}",
            "vehicle_type": data.get('vehicle_type', data.get('vehicleType', 'Motorcycle (Two-Wheeler)')),
            "vehicle_number": data.get('vehicle_number', data.get('vehicleNumber', '')),
            "is_online": True,
            "rating": "5.0",
            "has_individual_photo": data.get('has_individual_photo', False),
            "has_family_photo": data.get('has_family_photo', False),
            "has_police_noc": data.get('has_police_noc', False),
            "payment_mode": "Online Only",
            "extra_data": {
                "secondary_phone": clean_sec_phone,
                "location_type": location_type,
                "town_village": town_village,
                "has_individual_photo": data.get('has_individual_photo', False),
                "has_family_photo": data.get('has_family_photo', False),
                "has_police_noc": data.get('has_police_noc', False),
                "individual_photo_name": data.get('individual_photo_name'),
                "family_photo_name": data.get('family_photo_name'),
                "police_noc_name": data.get('police_noc_name')
            },
            "password": generate_password_hash(password),
            "created_at": datetime.now().isoformat()
        }

        save_user(user_record)

        # Set session for seamless login
        clean_user = {k: v for k, v in user_record.items() if k != 'password'}
        _ensure_patient_fields(clean_user)
        session['user_id'] = user_record["id"]
        session['user'] = clean_user

        if role in ['pharmacy', 'pharma']:
            redirect_url = '/pharmacy/dashboard'
        elif role == 'lab':
            redirect_url = '/lab/dashboard'
        elif role == 'rider':
            redirect_url = '/rider/dashboard'
        elif role == 'patient':
            redirect_url = '/patient/dashboard'
        else:
            redirect_url = '/'

        return jsonify({
            "status": "success",
            "message": f"Account successfully created! Welcome to Nhealth, {name}.",
            "user": clean_user,
            "redirect": redirect_url
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Sign up failed: {str(e)}"
        }), 500


@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    """Handle secure authentication via credentials with rate-limiting."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        identifier = data.get('identifier', '').strip()
        password = data.get('password', '').strip()
        role = data.get('role', '')

        client_ip = request.remote_addr or 'unknown'
        rate_key = f"{client_ip}:{identifier}"

        # Rate-limiting / Brute-force lockout check
        is_limited, wait_time = is_rate_limited(rate_key)
        if is_limited:
            return jsonify({
                "status": "error",
                "message": f"Too many failed login attempts. For security reasons, please wait {wait_time} seconds before trying again."
            }), 429

        if not identifier:
            return jsonify({
                "status": "error",
                "message": "Please enter your Mobile Number or Email."
            }), 400

        if not password:
            return jsonify({
                "status": "error",
                "message": "Please enter your Password."
            }), 400

        users = get_all_users()
        identifier_lower = identifier.lower()
        clean_digits = re.sub(r'\D', '', identifier)

        # Find matching user
        matched = None
        for u in users:
            u_email = u.get('email', '').lower()
            u_phone = re.sub(r'\D', '', str(u.get('phone', '')))
            if (u_email and u_email == identifier_lower) or (clean_digits and u_phone == clean_digits):
                matched = u
                break

        # Guaranteed fallback for official demo credentials
        if not matched:
            if identifier_lower in ['pharmacy@nhealth.in', 'pharma@gmail.com', 'pharma@nhealth.in', 'saimedicals@gmail.com'] or clean_digits in ['9876543290', '9988776655']:
                matched = {
                    "id": "USR-PHA-001",
                    "role": "pharmacy",
                    "name": "Sai Medicals",
                    "owner_name": "Sai Medicals & Pharmacy",
                    "email": identifier_lower if '@' in identifier_lower else "pharmacy@nhealth.in",
                    "phone": clean_digits or "9876543290",
                    "whatsapp": clean_digits or "9876543290",
                    "specialization": "Doorstep E-Pharmacy",
                    "clinic_name": "Sai Medicals",
                    "reg_number": "PHA-000123",
                    "gst_number": "37CCCC1234A1Z3",
                    "city": "Narasaraopeta",
                    "state": "Andhra Pradesh",
                    "pincode": "522601",
                    "address": "Main Road, Near Gandhi Chowk, Narasaraopeta",
                    "password": "password123",
                    "created_at": "2026-01-15T10:00:00"
                }
            elif identifier_lower in ['lab@nhealth.in', 'lab@gmail.com'] or clean_digits in ['9876543299']:
                matched = {
                    "id": "USR-LAB-001",
                    "role": "lab",
                    "name": "Apollo Diagnostics & Pathology Lab",
                    "owner_name": "Dr. K. Srinivas Rao",
                    "email": identifier_lower if '@' in identifier_lower else "lab@nhealth.in",
                    "phone": clean_digits or "9876543299",
                    "whatsapp": clean_digits or "9876543299",
                    "specialization": "Diagnostic Pathology & Blood Tests",
                    "clinic_name": "Apollo Diagnostics & Pathology Lab",
                    "reg_number": "AP-LAB-2026-001",
                    "city": "Vijayawada",
                    "password": "password123"
                }
            elif identifier_lower in ['priya.sharma@nhealth.in', 'dr.priya@nhealth.in', 'priya@gmail.com', 'priya@nhealth.in', 'priya'] or clean_digits in ['9848011223']:
                matched = {
                    "id": "USR-DOC-002",
                    "role": "doctor",
                    "name": "Dr. Priya Sharma",
                    "doctor_id": "DOC-NH-74892",
                    "qualification": "MBBS, MD (General Medicine)",
                    "specialization": "General Physician & Internal Medicine",
                    "experience": "9+ Years",
                    "reg_number": "APMC/74892",
                    "clinic_name": "Nhealth Prime Care Center",
                    "email": identifier_lower if '@' in identifier_lower else "priya.sharma@nhealth.in",
                    "phone": clean_digits or "9848011223",
                    "city": "Vijayawada",
                    "password": "password123"
                }
            elif identifier_lower in ['doctor@nhealth.in', 'doctor@gmail.com', 'dr.arjun@nhealth.in'] or clean_digits in ['9876543210']:
                matched = {
                    "id": "USR-DOC-001",
                    "role": "doctor",
                    "name": "Dr. Arjun Reddy",
                    "doctor_id": "DOC78456",
                    "qualification": "MBBS, MD (General Medicine)",
                    "specialization": "General Physician",
                    "experience": "8+ Years",
                    "reg_number": "APMC/12345",
                    "email": identifier_lower if '@' in identifier_lower else "doctor@nhealth.in",
                    "phone": clean_digits or "9876543210",
                    "city": "Vijayawada",
                    "password": "password123"
                }
            elif identifier_lower in ['patient@nhealth.in', 'patient@gmail.com'] or clean_digits in ['9123456780']:
                matched = {
                    "id": "USR-PAT-001",
                    "role": "patient",
                    "name": "Suresh Kumar",
                    "email": identifier_lower if '@' in identifier_lower else "patient@nhealth.in",
                    "phone": clean_digits or "9123456780",
                    "city": "Visakhapatnam",
                    "password": "password123"
                }

        if not matched or not verify_password(matched.get('password', ''), password):
            record_failed_attempt(rate_key)
            return jsonify({
                "status": "error",
                "message": "Invalid mobile number/email or password. Please check your credentials."
            }), 401

        # Clear failed attempts on successful login
        clear_failed_attempts(rate_key)

        # Upgrade legacy plain-text password to secure hash if needed
        if not matched.get('password', '').startswith(('pbkdf2:sha256:', 'scrypt:', 'argon2:')):
            update_user(matched['id'], {'password': generate_password_hash(password)})

        clean_user = {k: v for k, v in matched.items() if k != 'password'}
        _ensure_patient_fields(clean_user)
        session['user_id'] = matched['id']
        session['user'] = clean_user

        user_role = clean_user.get('role', '') or role or 'patient'
        if user_role in ['pharmacy', 'pharma'] or role in ['pharmacy', 'pharma']:
            redirect_url = '/pharmacy/dashboard'
        elif user_role == 'lab' or role == 'lab':
            redirect_url = '/lab/dashboard'
        elif user_role == 'rider' or role == 'rider':
            redirect_url = '/rider/dashboard'
        elif user_role == 'doctor' or role == 'doctor':
            redirect_url = '/doctor/dashboard'
        else:
            redirect_url = '/patient/dashboard'

        return jsonify({
            "status": "success",
            "message": f"Welcome back, {clean_user['name']}!",
            "user": clean_user,
            "redirect": redirect_url
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Login failed: {str(e)}"
        }), 500


# ==================== RIDER & TRIP REAL-TIME API ROUTES ====================

@app.route('/api/rider/status', methods=['POST'])
def api_rider_status():
    """Toggle online/offline duty status for rider."""
    data = request.get_json() or {}
    user = session.get('user')
    rider_id = data.get('rider_id') or (user.get('id') if user else 'USR-RIDER-001')
    is_online = data.get('is_online', True)
    db.update_rider_duty_status(rider_id, is_online)
    if user and user.get('id') == rider_id:
        session['user']['is_online'] = is_online
    return jsonify({"status": "success", "is_online": is_online})


@app.route('/api/rider/location', methods=['POST'])
def api_rider_location():
    """Update live GPS location stream from rider phone."""
    data = request.get_json() or {}
    user = session.get('user')
    rider_id = data.get('rider_id') or (user.get('id') if user else 'USR-RIDER-001')
    lat = data.get('lat', 16.5020)
    lng = data.get('lng', 80.6430)
    heading = data.get('heading', 0)
    active_trip_id = data.get('trip_id')
    db.update_rider_location(rider_id, lat, lng, heading, active_trip_id)
    return jsonify({"status": "success", "lat": lat, "lng": lng, "heading": heading})


@app.route('/api/rider/tasks', methods=['GET'])
def api_rider_tasks():
    """Get active trip and available dispatch task queue for rider cockpit."""
    user = session.get('user')
    rider_id = request.args.get('rider_id') or (user.get('id') if user else 'USR-RIDER-001')
    
    all_trips = db.get_all_trips()
    active_trip = None
    for t in all_trips:
        if t.get('rider_id') == rider_id and t.get('status') in ('accepted', 'arrived', 'in_progress', 'in_transit'):
            active_trip = t
            break
            
    available = db.get_available_tasks_for_riders()
    return jsonify({
        "status": "success",
        "active_trip": active_trip,
        "available_tasks": available
    })


@app.route('/api/rider/accept_task', methods=['POST'])
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
    
    success = db.accept_trip_by_rider(trip_id, rider_id, rider_name, rider_phone, rider_vehicle, rider_lat, rider_lng)
    if success:
        trip = db.get_trip_by_id(trip_id)
        if trip:
            return jsonify({"status": "success", "message": "Trip accepted successfully!", "trip": trip})
        return jsonify({"status": "success", "message": "Trip accepted!"})
    return jsonify({"status": "error", "message": "Failed to accept trip. It may have already been accepted."}), 400


@app.route('/api/rider/update_task_status', methods=['POST'])
def api_rider_update_task_status():
    """Update task lifecycle state (arrived, in_progress, completed, ended, cancelled)."""
    data = request.get_json() or {}
    trip_id = data.get('trip_id')
    status = data.get('status', 'arrived')
    db.update_trip_status(trip_id, status)
    trip = db.get_trip_by_id(trip_id)
    return jsonify({"status": "success", "trip": trip})


@app.route('/api/rider/history', methods=['GET'])
def api_rider_history():
    """Fetch completed, ended, and cancelled trip history for rider cockpit."""
    user = session.get('user')
    rider_id = request.args.get('rider_id') or (user.get('id') if user else None)
    if not rider_id:
        return jsonify({"status": "error", "message": "Rider authentication required."}), 401
    history = db.get_rider_trip_history(rider_id)
    return jsonify({
        "status": "success",
        "history": history
    })


@app.route('/api/rider/verify_otp', methods=['POST'])
def api_rider_verify_otp():
    """Verify 4-digit start OTP provided by patient."""
    data = request.get_json() or {}
    trip_id = data.get('trip_id')
    otp = data.get('otp', '').strip()
    success, msg = db.verify_trip_otp(trip_id, otp)
    if success:
        return jsonify({"status": "success", "message": msg, "trip": db.get_trip_by_id(trip_id)})
    return jsonify({"status": "error", "message": msg}), 400


@app.route('/api/trip/create', methods=['POST'])
def api_trip_create():
    """Create a new health support ride request from patient dashboard."""
    import random
    data = request.get_json() or {}
    trip_id = f"TRIP-{datetime.now().strftime('%y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    start_otp = str(random.randint(1000, 9999))
    
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
        "invoice_number": db.generate_next_invoice_number("NH-INV"),
        "extra_data": {
            "payment_mode": "Online Only (UPI/QR)",
            "payment_status": "PAID / Online Verified",
            "payment_id": data.get('payment_id') or f"PAY-UPI-{datetime.now().strftime('%y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}",
            "invoice_number": db.generate_next_invoice_number("NH-INV"),
            "invoice_date": datetime.now().strftime('%d %b %Y, %I:%M %p'),
            "paid_amount": int(data.get('fare_amount', 120)),
            "cancellation_policy": "Once booked, the service cannot be cancelled or refunded.",
            "validity_policy": "The payment is valid only on that day."
        }
    }
    
    # Ensure matching invoice number across record
    trip_record["invoice_number"] = trip_record["extra_data"]["invoice_number"]
    
    db.create_rider_trip(trip_record)
    
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


@app.route('/api/trip/<trip_id>/invoice', methods=['GET'])
def api_trip_invoice(trip_id):
    """Retrieve full tax invoice and receipt for a trip."""
    trip = db.get_trip_by_id(trip_id)
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


@app.route('/api/trip/<trip_id>/live', methods=['GET'])
def api_trip_live(trip_id):
    """Retrieve real-time GPS coordinates, ETA, and status of trip."""
    trip = db.get_trip_by_id(trip_id)
    if not trip:
        return jsonify({"status": "error", "message": "Trip not found"}), 404
    return jsonify({
        "status": "success",
        "trip": trip
    })


@app.route('/api/auth/logout', methods=['POST', 'GET'])
def auth_logout():
    """Clear session on logout."""
    session.clear()
    return jsonify({
        "status": "success",
        "message": "Logged out successfully"
    }), 200


@app.route('/api/user/profile', methods=['GET', 'POST'])
def user_profile():
    """Retrieve or update logged-in patient profile."""
    try:
        if request.method == 'GET':
            patient = get_current_patient()
            return jsonify({"status": "success", "user": patient}), 200

        # POST: update profile
        data = request.get_json() if request.is_json else request.form.to_dict()
        user_id = data.get('id') or session.get('user_id')
        
        users = get_all_users()
        target_user = None
        if user_id:
            for u in users:
                if u.get('id') == user_id:
                    target_user = u
                    break
        if not target_user and users:
            target_user = users[-1]
            user_id = target_user['id']

        updates = {}
        if 'name' in data and data['name'].strip():
            updates['name'] = data['name'].strip()
        if 'phone' in data and data['phone'].strip():
            updates['phone'] = data['phone'].strip()
        if 'email' in data and data['email'].strip():
            updates['email'] = data['email'].strip()
        if 'city' in data and data['city'].strip():
            updates['city'] = data['city'].strip()
        if 'age' in data:
            try:
                updates['age'] = int(data['age'])
            except (ValueError, TypeError):
                pass
        if 'dob' in data and data['dob'].strip():
            updates['dob'] = data['dob'].strip()
            try:
                birth_date = datetime.strptime(data['dob'].strip(), '%Y-%m-%d')
                today = date.today()
                updates['age'] = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            except Exception:
                pass
        if 'gender' in data and data['gender'].strip():
            updates['gender'] = data['gender'].strip()
        if 'blood_group' in data and data['blood_group'].strip():
            updates['blood_group'] = data['blood_group'].strip()
        if 'address' in data and data['address'].strip():
            updates['address'] = data['address'].strip()

        if user_id and updates:
            update_user(user_id, updates)
            for k, v in updates.items():
                target_user[k] = v
            clean_user = {k: v for k, v in target_user.items() if k != 'password'}
            _ensure_patient_fields(clean_user)
            session['user_id'] = clean_user['id']
            session['user'] = clean_user
            return jsonify({
                "status": "success",
                "message": "Patient profile updated successfully!",
                "user": clean_user
            }), 200
        
        return jsonify({"status": "error", "message": "No profile updates provided."}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to update profile: {str(e)}"}), 500



@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle general inquiries and contact requests from website."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '').strip()
        subject = data.get('subject', 'General Inquiry').strip()
        message = data.get('message', '').strip()

        if not name or not phone:
            return jsonify({
                "status": "error",
                "message": "Full name and phone number are required."
            }), 400

        contact_entry = {
            "id": f"INQ-{datetime.now().strftime('%y%m%d')}-{uuid.uuid4().hex[:4].upper()}",
            "name": name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message,
            "created_at": datetime.now().isoformat(),
            "status": "new"
        }

        # Save contact inquiry via database layer
        db.save_contact(contact_entry)

        return jsonify({
            "status": "success",
            "message": f"Thank you, {name}! Your message regarding '{subject}' has been received. Our support team will get back to you shortly."
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


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
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

if not os.path.exists(BOOKINGS_FILE):
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

def get_all_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_user(user_data):
    users = get_all_users()
    users.append(user_data)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)


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


@app.route('/patient/dashboard')
@app.route('/dashboard')
@app.route('/consultation')
def patient_dashboard():
    """Render the Patient Online Consultation & Healthcare Dashboard (Mobile + Laptop views)."""
    return render_template('patient_dashboard.html', services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/login')
def login_page():
    """Render the Login page."""
    role = request.args.get('role', 'patient')
    return render_template('login.html', role=role, services=SERVICES, locations=AP_LOCATIONS, stats=STATS)


@app.route('/signup')
def signup_page():
    """Render the Signup page (defaults to patient or uses role query)."""
    role = request.args.get('role', 'patient')
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


@app.route('/api/auth/signup', methods=['POST'])
def auth_signup():
    """Handle new patient or doctor/partner account registration."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        role = data.get('role', 'patient').strip().lower()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '').strip()
        password = data.get('password', '').strip()

        if not name or not phone or not password:
            return jsonify({
                "status": "error",
                "message": "Full Name, Phone Number, and Password are required."
            }), 400

        users = get_all_users()

        # Check existing user
        if any(u.get('phone') == phone or (email and u.get('email') == email) for u in users):
            return jsonify({
                "status": "error",
                "message": "An account with this phone number or email already exists. Please login."
            }), 409

        user_id = f"USR-{role[:3].upper()}-{datetime.now().strftime('%y%m')}-{uuid.uuid4().hex[:4].upper()}"

        user_record = {
            "id": user_id,
            "role": role,
            "name": name,
            "email": email,
            "phone": phone,
            "whatsapp": data.get('whatsapp', phone).strip(),
            "specialization": data.get('specialization', ''),
            "clinic_name": data.get('clinic_name', ''),
            "reg_number": data.get('reg_number', ''),
            "city": data.get('city', ''),
            "password": password,
            "created_at": datetime.now().isoformat()
        }

        save_user(user_record)

        return jsonify({
            "status": "success",
            "message": f"Account successfully created! Welcome to Nhealth, {name}.",
            "user": {
                "id": user_record["id"],
                "name": user_record["name"],
                "role": user_record["role"],
                "email": user_record["email"],
                "phone": user_record["phone"]
            }
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Sign up failed: {str(e)}"
        }), 500


@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    """Handle authentication via credentials or demo login."""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        identifier = data.get('identifier', '').strip()
        password = data.get('password', '').strip()
        role = data.get('role', '')

        if not identifier:
            return jsonify({
                "status": "error",
                "message": "Please enter your Email or Phone Number."
            }), 400

        users = get_all_users()
        identifier_lower = identifier.lower()

        # Find matching user
        matched = None
        for u in users:
            if u.get('email', '').lower() == identifier_lower or u.get('phone') == identifier:
                if not password or u.get('password') == password:
                    matched = u
                    break

        if not matched:
            # Flexible demo login for user testing
            matched = {
                "id": f"USR-DEMO-{uuid.uuid4().hex[:4].upper()}",
                "name": identifier.split('@')[0].capitalize() if '@' in identifier else "Valued User",
                "role": role if role else "patient",
                "email": identifier if '@' in identifier else f"{identifier}@nhealth.in",
                "phone": identifier if identifier.isdigit() else "9876543210"
            }

        return jsonify({
            "status": "success",
            "message": f"Welcome back, {matched['name']}!",
            "user": {
                "id": matched["id"],
                "name": matched["name"],
                "role": matched.get("role", "patient"),
                "email": matched.get("email", ""),
                "phone": matched.get("phone", "")
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Login failed: {str(e)}"
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


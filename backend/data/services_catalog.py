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

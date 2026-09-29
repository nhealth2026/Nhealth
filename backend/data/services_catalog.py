"""
Comprehensive Healthcare Services Catalog for Nhealth
Enriched with detailed clinical matter, hero images, workflow steps, pricing, and FAQs.
"""

SERVICES = [
    {
        "id": "online-consult",
        "slug": "online-consult",
        "title": "Online Doctor Consultation",
        "category": "Doctor Consultation",
        "filter_cat": "doctor",
        "icon": "user-doctor",
        "emoji": "🩺",
        "color": "#0ea5e9",
        "bg_tint": "rgba(14, 165, 233, 0.12)",
        "badge": "15-Min Connect",
        "hero_image": "images/services/hero/online-consult.jpg",
        "art_image": "images/services/srv_online_consult.png",
        "tagline": "Connect with 1,500+ Board-Certified Physicians in 15 Minutes",
        "description": "Connect instantly with 1,500+ board-certified general physicians and super-specialists via secure, encrypted HD video or phone within 15 minutes.",
        "detailed_overview": (
            "Nhealth's Online Doctor Consultation brings certified clinical medical expertise straight to your smartphone or laptop. "
            "Whether you need an immediate general physician assessment for acute symptoms (fever, cough, migraine, digestion) or ongoing super-specialty management "
            "(Cardiology, Dermatology, Pediatrics, Gynecology, Endocrinology), our encrypted telemedicine clinic provides zero-waiting-room access. "
            "Every consultation is conducted by verified practitioners registered with state medical councils and includes real-time vital telemetry review, "
            "synchronized clinical chat, and a digitally signed e-prescription compliant with national telemedicine guidelines."
        ),
        "clinical_scope": [
            "General Medicine: Fever, Infections, Body Aches, Cold & Flu",
            "Cardiology & Hypertension: BP Management & Chest Discomfort Review",
            "Dermatology: Acne, Skin Rashes, Allergies & Hair Fall",
            "Pediatrics & Child Care: Infant Nutrition, Fevers & Common Illnesses",
            "Gynecology & Women's Health: PCOD/PCOS, Menstrual Irregularities & Prenatal Advice",
            "Diabetology & Endocrinology: Blood Sugar Control & Thyroid Management"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Select Specialty & Share Symptoms",
                "desc": "Choose your required medical department, describe your symptoms, or upload previous medical records and test reports."
            },
            {
                "step": "2",
                "title": "Connect in 15 Minutes",
                "desc": "Join a high-definition encrypted 1-on-1 video room with a verified doctor. Discuss symptoms, vitals, and family medical history."
            },
            {
                "step": "3",
                "title": "Instant E-Prescription & 7-Day Follow-Up",
                "desc": "Receive a verified digital prescription on WhatsApp and in your patient dashboard, plus enjoy 7 days of free follow-up chat."
            }
        ],
        "what_included": [
            "1-on-1 Encrypted HD Video Consultation (15-20 Minutes)",
            "Digitally Signed E-Prescription with MCI/NMC Registration Number",
            "Free Follow-Up Chat with Doctor for 7 Days",
            "Instant Medicine Order Sync with Doorstep Delivery",
            "Real-Time Vitals Review (BP, Pulse, SpO2, Temperature)"
        ],
        "benefits": [
            "15-Minute Guaranteed Doctor Connect across Andhra Pradesh & India",
            "Zero Clinic Travel, Infection Exposure, or Waiting Room Hassle",
            "Multi-lingual Doctors: Telugu, English, Hindi & Regional Languages",
            "Automated WhatsApp Delivery of Clinical Summaries & Prescriptions"
        ],
        "pricing_info": "Consultation fees start at ₹299 (General Physician) to ₹599 (Super Specialists). Includes 7 days of free follow-up.",
        "faqs": [
            {
                "q": "How quickly can I connect to a doctor?",
                "a": "General physicians are available within 10 to 15 minutes of booking. Super-specialist appointments can be booked for immediate next-available slots or at your preferred time."
            },
            {
                "q": "Is the digital prescription legally valid at pharmacies?",
                "a": "Yes, 100%. Nhealth digital prescriptions are generated strictly adhering to the National Telemedicine Practice Guidelines and are accepted at all registered pharmacies and diagnostic centers across India."
            },
            {
                "q": "What happens if the call gets disconnected?",
                "a": "Our system features automatic reconnection. If disconnected, the doctor will call your registered mobile number directly or reconnect your video room immediately without any additional charges."
            }
        ],
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
        "slug": "doctor-home-visit",
        "title": "Doctor Home Visits",
        "category": "Doctor Consultation",
        "filter_cat": "doctor",
        "icon": "house-medical",
        "emoji": "👨‍⚕️",
        "color": "#10b981",
        "bg_tint": "rgba(16, 185, 129, 0.12)",
        "badge": "At Your Doorstep",
        "hero_image": "images/services/hero/doctor-home-visit.jpg",
        "art_image": "images/services/srv_doctor_visit.png",
        "tagline": "Senior MD Physicians Delivering Bedside Clinical Care at Your Home",
        "description": "Experienced MD physicians visit your home equipped with diagnostic kits for clinical physical checkups, chronic assessments, and bedside care.",
        "detailed_overview": (
            "When traveling to a crowded hospital is exhausting or clinically inadvisable—especially for elderly patients, bedridden individuals, "
            "or those recovering from major surgery—Nhealth Doctor Home Visits provide thorough bedside clinical care. "
            "Our licensed MD physicians arrive at your doorstep equipped with portable clinical examination kits (stethoscope, digital BP monitors, glucometers, pulse oximeters, and otoscopes). "
            "The doctor performs a comprehensive physical assessment, reviews chronic medications, evaluates vitals, and formulates an in-home medical management plan."
        ),
        "clinical_scope": [
            "Geriatric & Senior Citizen Physical Checkups",
            "Post-Surgical Discharge Follow-Up & Wound Evaluation",
            "Chronic Disease Monitoring (Diabetes, Hypertension, COPD, Kidney Ailments)",
            "Acute Bedside Illness Assessment (High Fever, Respiratory Distress, Dehydration)",
            "Palliative & Comfort Care Oversight",
            "Catheter & Ryle's Tube Clinical Inspection"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Schedule a Home Visit",
                "desc": "Select Doctor Home Visit, enter your address, specify the patient's condition, and choose a convenient time slot."
            },
            {
                "step": "2",
                "title": "MD Physician Arrives at Doorstep",
                "desc": "Our background-verified physician visits your residence with diagnostic kits, sanitization protocols, and medical supplies."
            },
            {
                "step": "3",
                "title": "Bedside Exam & Treatment Plan",
                "desc": "Physician conducts a complete 30-45 minute clinical examination, prescribes medications, and orders in-home nursing or lab tests if needed."
            }
        ],
        "what_included": [
            "Comprehensive 30-45 Minute In-Home Physical Examination",
            "Vital Parameters Screening (BP, SpO2, Blood Sugar, Temperature, Heart Sounds)",
            "Prescription Review & Medication Interaction Check",
            "Physical Assessment of Mobility & Surgical Sites",
            "Direct Coordination with Nhealth Doorstep Pharmacy & Lab Teams"
        ],
        "benefits": [
            "Eliminates Hospital Queue Fatigue for Frail & Senior Family Members",
            "Reduces Exposure to Hospital-Acquired Infections (HAIs)",
            "Unrushed Bedside Attention with Detailed Family Counseling",
            "Immediate In-Home Medical Prescriptions Delivered to Doorstep"
        ],
        "pricing_info": "Home visit fees start at ₹799 per visit. Includes comprehensive bedside examination and 3-day telephone follow-up.",
        "faqs": [
            {
                "q": "What cities is Doctor Home Visit currently available in?",
                "a": "Doctor Home Visits are actively operational across Vijayawada, Guntur, Visakhapatnam, Tirupati, Kurnool, Kakinada, and expanding throughout Andhra Pradesh."
            },
            {
                "q": "Can the visiting doctor administer injections or write tests?",
                "a": "Yes. Visiting physicians carry emergency medical kits, can administer intramuscular injections, and directly order portable X-rays, blood draws, or medicines for immediate home fulfillment."
            },
            {
                "q": "Is this service suitable for critical emergencies?",
                "a": "For life-threatening emergencies requiring ICU ventilation or immediate resuscitation, please use our 24/7 Smart Ambulance SOS service directly."
            }
        ],
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
        "slug": "pharmacy-home",
        "title": "Doorstep E-Pharmacy",
        "category": "Pharmacy & Medicines",
        "filter_cat": "pharmacy",
        "icon": "prescription-bottle-medical",
        "emoji": "💊",
        "color": "#059669",
        "bg_tint": "rgba(5, 150, 105, 0.12)",
        "badge": "2-Hour Express",
        "hero_image": "images/services/hero/pharmacy-home.jpg",
        "art_image": "images/services/srv_pharmacy.png",
        "tagline": "100% Genuine Certified Medicines Delivered to Your Doorstep in 2 Hours",
        "description": "Upload your prescription for instant pharmacist validation. Enjoy authentic temperature-controlled doorstep medicine delivery at discounted rates.",
        "detailed_overview": (
            "Nhealth Doorstep E-Pharmacy ensures you never run out of vital medications. "
            "Operating in partnership with certified retail pharmacies and temperature-monitored distribution hubs, we supply 100% genuine allopathic, ayurvedic, and surgical products. "
            "Whether you need an urgent dose of antibiotics or monthly refills for chronic cardiac, hypertension, or diabetic medications, our pharmacists inspect your prescription, "
            "verify drug interactions, and dispatch tamper-evident sealed packages with 2-hour express delivery guarantees."
        ),
        "clinical_scope": [
            "Chronic Disease Maintenance Refills (Hypertension, Diabetes, Cardiac, Thyroid)",
            "Acute Prescriptions (Antibiotics, Analgesics, Respiratory Inhalers, Eye Drops)",
            "Temperature-Controlled Cold-Chain Items (Insulin Pens, Biologics, Vaccines)",
            "Surgical & Wound Care Supplies (Sterile Gauze, Betadine, Micropore, Syringes)",
            "Specialized Nutrition & Elderly Dietary Supplements",
            "Medical Devices (Glucometers, BP Monitors, Nebulizers, Pulse Oximeters)"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Upload Prescription",
                "desc": "Take a photo of your doctor's prescription or choose from your recent online consultation records in your dashboard."
            },
            {
                "step": "2",
                "title": "Pharmacist Review & Bill Confirmation",
                "desc": "A registered pharmacist validates the dosage, checks stock, and shares an itemized bill with automatic discounts applied."
            },
            {
                "step": "3",
                "title": "2-Hour Express Doorstep Delivery",
                "desc": "Our delivery agent delivers sealed medicines directly to your door with temperature-safe cold packs when needed."
            }
        ],
        "what_included": [
            "100% Genuine Certified Medicines from Licensed Distributors",
            "Professional Pharmacist Validation & Drug Interaction Check",
            "Flat 15% to 20% Discount on Monthly Chronic Medicine Refills",
            "Temperature-Controlled Cold-Chain Packaging for Insulin & Vials",
            "Automated Monthly WhatsApp Refill Reminders"
        ],
        "benefits": [
            "Guaranteed 2-Hour Express Delivery Across City Limits",
            "Zero Risk of Counterfeit or Substandard Medicines",
            "GST Compliant Detailed Invoice for Medical Insurance & Reimbursements",
            "Seamless WhatsApp and Online Payment Support"
        ],
        "pricing_info": "Free doorstep delivery on all orders above ₹499. Flat 15-20% discount on all chronic prescription medicines.",
        "faqs": [
            {
                "q": "Do I need a prescription to order medicines?",
                "a": "Prescription medications (Schedule H and H1 drugs) strictly require a valid doctor's prescription. OTC wellness items and medical devices can be ordered directly without a prescription."
            },
            {
                "q": "How do you maintain the cold chain for insulin?",
                "a": "Insulin, vaccines, and biologicals are packed in specialized insulated thermocool pouches with frozen ice packs and delivered directly to maintain 2°C to 8°C throughout transit."
            },
            {
                "q": "Can I set up automatic monthly refills for my parents?",
                "a": "Yes! Our automated chronic refill service alerts you 3 days before medications run out, allowing 1-click WhatsApp reordering."
            }
        ],
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
        "slug": "lab-tests-home",
        "title": "Home Diagnostics & Lab Tests",
        "category": "Diagnostics & Lab",
        "filter_cat": "diagnostics",
        "icon": "flask-vial",
        "emoji": "🔬",
        "color": "#0284c7",
        "bg_tint": "rgba(2, 132, 199, 0.12)",
        "badge": "NABL Accredited",
        "hero_image": "images/services/hero/lab-tests-home.jpg",
        "art_image": "images/services/srv_lab_tests.png",
        "tagline": "Painless Home Sample Collection with Verified Smart Reports in 6 Hours",
        "description": "Certified phlebotomists arrive at your doorstep with sealed vacutainer kits for blood, urine, and pathology sample collection with fast digital reports.",
        "detailed_overview": (
            "Accurate diagnosis is the foundation of effective medical treatment. Nhealth Home Diagnostics connects you with NABL & CAP accredited pathology laboratories. "
            "Trained, certified phlebotomists arrive at your home with sterile, single-use vacuum collection tubes and barcoded collection vials. "
            "Whether you require fasting blood sugar, complete blood count (CBC), lipid profile, liver function (LFT), kidney function (KFT), or advanced thyroid panels, "
            "your samples are preserved in temperature-controlled transport bags and processed using automated analyzers, delivering smart digital PDF reports in under 6 hours."
        ),
        "clinical_scope": [
            "Complete Blood Count (CBC) with ESR & Peripheral Smear",
            "Diabetes Profiling: Fasting Blood Sugar, PPBS, and HbA1c",
            "Lipid Profile: Cholesterol, HDL, LDL, VLDL & Triglycerides",
            "Liver Function Tests (LFT) & Kidney Function Tests (KFT/RFT)",
            "Thyroid Profile: Total & Free T3, T4, and Ultra-sensitive TSH",
            "Vitamins: Vitamin D3 (25-OH) & Vitamin B12 Levels",
            "Infectious Disease: Dengue NS1/IgM, Malaria, Typhoid, Viral Panels"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Choose Tests or Health Package",
                "desc": "Select individual pathology tests or cost-saving full-body health profiles. Choose morning fasting or anytime slots."
            },
            {
                "step": "2",
                "title": "Painless In-Home Sample Collection",
                "desc": "Our certified phlebotomist arrives with sealed single-use vacutainer needles and barcoded tubes for safe blood/urine collection."
            },
            {
                "step": "3",
                "title": "Verified Digital Report in 6 Hours",
                "desc": "Sample is analyzed at NABL accredited labs. Verified PDF report is sent directly to WhatsApp and your dashboard with doctor consultation options."
            }
        ],
        "what_included": [
            "Painless Blood Draw by Background-Verified Certified Phlebotomist",
            "Sterile, Barcoded Vacuum Tubes (Zero Contamination Risk)",
            "NABL / CAP Certified Automated Pathology Processing",
            "Smart PDF Digital Report Delivered in 6 Hours via WhatsApp",
            "Free Follow-up Report Analysis by Physician"
        ],
        "benefits": [
            "No Fasting Commutes or Long Waiting Queues at Diagnostic Centers",
            "Precise Results Benchmarked Against International Reference Standards",
            "Specialized Pediatric & Geriatric Phlebotomy Specialists",
            "Competitive Pricing with up to 50% Savings Compared to Hospital Walk-ins"
        ],
        "pricing_info": "Individual tests start from ₹199. Full body comprehensive screening packages starting from ₹699.",
        "faqs": [
            {
                "q": "Do I need to fast before the sample collection?",
                "a": "Tests such as Fasting Blood Sugar (FBS) and Lipid Profile require 8-10 hours of overnight fasting (water is permitted). Other tests like HbA1c and CBC do not require fasting."
            },
            {
                "q": "Are the reports accepted by hospital specialists?",
                "a": "Yes. All samples are analyzed at NABL & CAP accredited partner laboratories and are universally recognized by doctors and hospitals across India."
            },
            {
                "q": "How can I access my lab reports?",
                "a": "As soon as the pathologist verifies your results, an encrypted PDF is sent directly to your WhatsApp and permanently stored in your Nhealth Patient Dashboard."
            }
        ],
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
        "slug": "xray-at-home",
        "title": "X-Ray & Portable Diagnostics",
        "category": "Diagnostics & Lab",
        "filter_cat": "diagnostics",
        "icon": "radiation",
        "emoji": "🩻",
        "color": "#6366f1",
        "bg_tint": "rgba(99, 102, 241, 0.12)",
        "badge": "Portable Digital",
        "hero_image": "images/services/hero/xray-at-home.jpg",
        "art_image": "images/services/srv_xray.png",
        "tagline": "Advanced Low-Radiation Digital X-Ray & 12-Lead ECG at Your Bedside",
        "description": "Advanced low-radiation portable digital X-Ray and 12-lead ECG machines brought straight to your bedroom for immediate imaging without traveling.",
        "detailed_overview": (
            "Moving an elderly patient with a suspected bone fracture, painful arthritis, or severe pneumonia to an imaging center can aggravate injuries. "
            "Nhealth Portable Digital Diagnostics brings cutting-edge, low-radiation bedside digital radiography and 12-lead digital ECG straight to the patient's bedroom. "
            "Our certified radiological technicians set up portable high-frequency X-Ray equipment in minutes, capture high-resolution DICOM digital plates, "
            "and upload them immediately to board-certified radiologists for instant clinical reporting."
        ),
        "clinical_scope": [
            "Chest X-Ray: Pneumonia, Chronic Bronchitis, Pleural Effusion & Congestion",
            "Orthopedic Imaging: Suspected Hip, Spine, Knee & Shoulder Fractures",
            "Post-Surgical Implant & Joint Replacement Bedside Evaluation",
            "12-Lead Digital ECG: Cardiac Arrhythmia, Ischemia & Routine Check",
            "Bedside Imaging for Non-Ambulatory & Stroke Patients"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Book Bedside X-Ray / ECG",
                "desc": "Select the required body region (Chest, Spine, Hip, Extremities) or 12-Lead ECG and provide doctor prescription."
            },
            {
                "step": "2",
                "title": "Technician Arrives with Portable Device",
                "desc": "A licensed radiological technologist arrives with shielded portable equipment and captures digital images in your bedroom."
            },
            {
                "step": "3",
                "title": "Instant Radiologist Report",
                "desc": "DICOM digital films are transmitted to our senior radiologist. You receive verified digital films and report within 2 to 4 hours."
            }
        ],
        "what_included": [
            "Certified Radiological Technologist In-Home Visit",
            "High-Frequency Ultra-Low Radiation Digital X-Ray System",
            "High-Resolution DICOM Digital Radiography Plate",
            "Detailed Radiologist Second-Opinion Diagnostic Report",
            "Instant Digital Film Download Link via WhatsApp"
        ],
        "benefits": [
            "Eliminates Painful Ambulance Transfers for Suspected Fractures",
            "Safe for Elderly & Bedridden Patients in Home Comfort",
            "Lead-Shielded Safety Protocols Ensuring Zero Radiation for Family",
            "Rapid Radiologist Turnaround for Immediate Orthopedic Decisions"
        ],
        "pricing_info": "Chest X-Ray starts at ₹1,299 per view. 12-Lead Digital ECG at ₹599. Combined packages available.",
        "faqs": [
            {
                "q": "Is portable X-Ray safe inside a residential home?",
                "a": "Yes. Our portable systems utilize focused collimators and ultra-sensitive digital detectors requiring a fraction of the radiation of traditional hospital units. Technicians deploy lead shielding to ensure complete safety."
            },
            {
                "q": "How fast do we receive the X-ray films and report?",
                "a": "The digital films are visible on the technician's screen immediately after the exposure. The official signed radiologist report is delivered via WhatsApp in 2 to 4 hours."
            },
            {
                "q": "Can multiple views (e.g. Chest AP and Lateral) be taken in one visit?",
                "a": "Yes, our technician can perform multiple anatomical views as directed by your physician during the same visit."
            }
        ],
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
        "slug": "nursing-services",
        "title": "Specialized Nursing Care",
        "category": "Home Care & Nursing",
        "filter_cat": "nursing",
        "icon": "user-nurse",
        "emoji": "👩‍⚕️",
        "color": "#ec4899",
        "bg_tint": "rgba(236, 72, 153, 0.12)",
        "badge": "GNM / B.Sc Certified",
        "hero_image": "images/services/hero/nursing-services.jpg",
        "art_image": "images/services/srv_nursing.png",
        "tagline": "Qualified Registered Nurses Providing Hospital-Grade Clinical Care at Home",
        "description": "Compassionate, qualified registered nurses for post-operative recovery, elderly assistance, wound dressing, catheter management, and home ICU.",
        "detailed_overview": (
            "Nhealth Specialized Nursing Care bridges the gap between hospital discharge and full recovery. "
            "Our registered nurses (GNM / B.Sc Nursing certified) are trained in critical clinical procedures, sterile wound management, and home intensive care. "
            "Available in flexible 12-hour day/night shifts and 24-hour residential stays, our nurses administer IV medications, oversee tracheostomy care, "
            "manage urinary catheters and Ryle's tube feeding, track patient vitals every hour, and coordinate directly with your primary physician to prevent readmissions."
        ),
        "clinical_scope": [
            "Post-Operative & Post-Surgical Healing & Wound Dressing",
            "Home ICU & Critical Care: Oxygen Therapy, BiPAP, CPAP, Tracheostomy",
            "IV Cannulation, IV Infusions & Injectable Medication Administration",
            "Foley's Urinary Catheterization & Bladder Wash",
            "Enteral Feeding: Ryle's Tube & PEG Tube Nutritional Support",
            "Diabetic Foot Ulcer Dressing & Bed Sore Prevention Protocols"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Clinical Assessment & Shift Selection",
                "desc": "Share patient discharge summary and requirements. Choose 12-hour day, 12-hour night, or 24-hour residential nursing care."
            },
            {
                "step": "2",
                "title": "Certified Nurse Assigned",
                "desc": "A background-verified, registered nurse tailored to the patient's medical needs (ICU trained, post-op, or geriatric) is deployed."
            },
            {
                "step": "3",
                "title": "Continuous Clinical Nursing",
                "desc": "The nurse executes physician orders, maintains hourly vital charts, administers sterile dressings, and delivers hospital-grade home care."
            }
        ],
        "what_included": [
            "Background-Verified GNM or B.Sc Registered Nurse",
            "Hourly Vital Signs Monitoring & Digital Charting (BP, SpO2, Pulse, Temp, Sugar)",
            "Sterile Dressing & Antiseptic Wound Care Protocol",
            "Medication Administration (Oral, IV, IM, Subcutaneous)",
            "Doctor Liaison & Emergency Escalation Management"
        ],
        "benefits": [
            "Reduces Costly Hospital ICU & Room Tariffs by up to 70%",
            "Accelerates Healing in Familiar, Stress-Free Home Surroundings",
            "Guaranteed 100% Background Check & Police Verification for All Staff",
            "Seamless Shift Replacements with Zero Interruption in Patient Care"
        ],
        "pricing_info": "12-hour day or night shifts starting from ₹1,200/shift. 24-hour residential nursing packages available with monthly discounts.",
        "faqs": [
            {
                "q": "What qualifications do your home nurses possess?",
                "a": "All our nurses hold recognized degrees in General Nursing and Midwifery (GNM) or B.Sc Nursing, are registered with state nursing councils, and have minimum 2 years of hospital experience."
            },
            {
                "q": "Can the nurse change a urinary catheter or Ryle's tube?",
                "a": "Yes. Our nurses are fully trained and certified in sterile catheterization, tube insertions, and dressing changes."
            },
            {
                "q": "What happens if a nurse is sick or on leave?",
                "a": "Our operations supervisor provides a pre-briefed backup nurse from our certified roster to ensure continuous, uninterrupted care."
            }
        ],
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
        "slug": "bedside-assistant",
        "title": "Bedside Assistant & Attendant",
        "category": "Home Care & Nursing",
        "filter_cat": "nursing",
        "icon": "bed-pulse",
        "emoji": "🛏️",
        "color": "#0d9488",
        "bg_tint": "rgba(13, 148, 136, 0.12)",
        "badge": "12hr & 24hr Shifts",
        "hero_image": "images/services/hero/bedside-assistant.jpg",
        "art_image": "images/services/srv_bedside.png",
        "tagline": "Compassionate Male & Female Attendants for Daily Hygiene, Feeding & Mobility",
        "description": "Trained male and female patient care attendants providing round-the-clock physical assistance, hygiene support, feeding, and mobility care at home.",
        "detailed_overview": (
            "Recovering from illness or living with chronic mobility limitations requires consistent, compassionate daily assistance. "
            "Nhealth Bedside Patient Attendants provide non-clinical personal care tailored for stroke survivors, post-surgery patients, fracture cases, and frail seniors. "
            "Our male and female attendants assist with bathing, bed sponge baths, oral hygiene, diaper changes, safe transfers between bed and wheelchair, "
            "assisted walking, feeding, and prompt medication reminders. Their presence ensures dignity, comfort, and peace of mind for family caregivers."
        ),
        "clinical_scope": [
            "Bedridden Patient Daily Sponge Bath & Oral Hygiene",
            "Diaper Changing, Bedpan Assistance & Incontinence Care",
            "Safe Patient Transfers (Bed to Wheelchair / Commode)",
            "Assisted Walking & Fall-Prevention Monitoring",
            "Nutritional Support & Feeding Assistance",
            "Medication Prompting & Turning to Prevent Pressure Bed Sores"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Specify Attendant Requirements",
                "desc": "Tell us the patient's gender, mobility level, and shift preference (12-hour day, night, or 24-hour live-in attendant)."
            },
            {
                "step": "2",
                "title": "Attendant Matching & Verification",
                "desc": "We match a trained, police-verified caregiver with appropriate experience in handling elderly or post-operative patients."
            },
            {
                "step": "3",
                "title": "Daily Compassionate Care",
                "desc": "The attendant arrives on time and manages hygiene, mobility, nutrition, and companionship with warmth and patience."
            }
        ],
        "what_included": [
            "Trained Patient Care Attendant (Male or Female as requested)",
            "Assistance with Personal Hygiene, Bathing & Grooming",
            "Bedpan Management, Diaper Changes & Sanitation",
            "Bed-to-Wheelchair Transfer Assistance",
            "Hourly Repositioning for Bed Sore Prevention"
        ],
        "benefits": [
            "Relieves Family Members from Exhausting Physical Caregiving Duties",
            "Professional Fall Prevention and Safe Transfer Techniques",
            "Background Checked, Police Verified, and Medical Fitness Certified Staff",
            "Affordable Long-Term Packages for Chronic Recovery"
        ],
        "pricing_info": "12-hour shifts starting from ₹750/day. 24-hour residential attendant packages from ₹1,200/day with weekly/monthly savings.",
        "faqs": [
            {
                "q": "Can I choose between a male or female attendant?",
                "a": "Yes. We respect patient comfort and privacy and provide verified male attendants for male patients and female attendants for female patients."
            },
            {
                "q": "Do attendants administer injections or manage IV lines?",
                "a": "No. Attendants handle non-clinical assistance (hygiene, mobility, feeding). For medical procedures like IV lines or catheterization, book our Specialized Nursing Care service."
            },
            {
                "q": "What happens if our family is not satisfied with the attendant?",
                "a": "We offer hassle-free caregiver replacements within 24 hours until your family is completely satisfied with the support."
            }
        ],
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
        "slug": "eldercare",
        "title": "Eldercare & Senior Assistance",
        "category": "Home Care & Nursing",
        "filter_cat": "nursing",
        "icon": "hands-holding-child",
        "emoji": "👵",
        "color": "#f97316",
        "bg_tint": "rgba(249, 115, 22, 0.12)",
        "badge": "Dedicated Companions",
        "hero_image": "images/services/hero/eldercare.jpg",
        "art_image": "images/services/srv_eldercare.png",
        "tagline": "Holistic Health, Companionship & Emergency Security for Aging Parents",
        "description": "Dedicated senior care companions and geriatric specialists helping your elderly loved ones live safely, healthily, and independently at home.",
        "detailed_overview": (
            "When career commitments or living in another city make daily hands-on care for aging parents challenging, Nhealth Eldercare provides a reliable family surrogate. "
            "Our holistic eldercare programmes pair your parents with compassionate senior companions and geriatric health coordinators. "
            "From monitoring daily vitals, coordinating monthly doctor visits, managing medication refills, and accompanying seniors on evening garden walks "
            "to 24/7 emergency SOS dispatch, we ensure your elderly parents enjoy active, dignified, and emotionally supported lives at home."
        ),
        "clinical_scope": [
            "Scheduled Geriatric Health & Vitals Monitoring",
            "Cognitive & Emotional Companionship (Reading, Walks, Conversations)",
            "Medication Adherence Management & Prescription Refill Logistics",
            "Accompanied OPD Visits & Diagnostic Centre Escort",
            "Dementia & Alzheimer's Supportive Home Care",
            "Home Safety Audits & Fall Prevention Measures"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Personalized Eldercare Assessment",
                "desc": "Our geriatric care specialist reviews your parents' medical history, lifestyle routines, and emotional needs."
            },
            {
                "step": "2",
                "title": "Care Buddy Assigned",
                "desc": "A dedicated, empathetic care companion is assigned to visit regularly or stay on scheduled daytime/residential shifts."
            },
            {
                "step": "3",
                "title": "Weekly Health Reports to Family",
                "desc": "Stay updated via WhatsApp with weekly vital logs, doctor consult notes, and daily wellbeing photos from our team."
            }
        ],
        "what_included": [
            "Dedicated Personal Care Buddy & Senior Companion",
            "Weekly In-Home Vitals Check & Health Status Documentation",
            "Monthly Doctor Video Consultation Included in Care Plan",
            "Priority Emergency Ambulance & Hospital Admission Escalation",
            "Detailed Weekly Digital Health Report for NRI / Distant Children"
        ],
        "benefits": [
            "Peace of Mind for Children Living Away from Elderly Parents",
            "Combats Loneliness, Depression & Social Isolation in Seniors",
            "Proactive Health Monitoring Prevents Sudden Emergency Hospitalizations",
            "24/7 Dedicated Helpline for Instant Parent Assistance"
        ],
        "pricing_info": "Flexible monthly eldercare membership packages starting from ₹2,999/month. Includes regular home visits and companion support.",
        "faqs": [
            {
                "q": "Can I subscribe to this plan for my parents from abroad (NRI)?",
                "a": "Yes! A large portion of our eldercare families are NRIs living in the USA, UK, and Middle East. We provide international online payment and send regular WhatsApp video and report updates."
            },
            {
                "q": "What happens if my parent has an emergency at night?",
                "a": "Our 24/7 emergency coordination team immediately dispatches the nearest smart ambulance, alerts the dedicated care buddy, and informs the family simultaneously."
            },
            {
                "q": "Do companions accompany parents to family functions or temples?",
                "a": "Yes. Our senior care companions can be booked to accompany elderly parents safely to temples, social visits, and hospital checkups."
            }
        ],
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
        "slug": "physiotherapy",
        "title": "Physiotherapy at Home",
        "category": "Rehabilitation & Therapy",
        "filter_cat": "rehab",
        "icon": "person-walking-with-cane",
        "emoji": "🚶‍♂️",
        "color": "#8b5cf6",
        "bg_tint": "rgba(139, 92, 246, 0.12)",
        "badge": "Certified Physios",
        "hero_image": "images/services/hero/physiotherapy.jpg",
        "art_image": "images/services/srv_physio.png",
        "tagline": "Specialized Bedside Physical Rehabilitation to Restore Mobility and Relieve Pain",
        "description": "Expert certified physiotherapists bringing specialized rehabilitation equipment to restore mobility, relieve chronic pain, and rebuild muscular strength.",
        "detailed_overview": (
            "Restoring pain-free movement after an orthopedic surgery, stroke, or chronic joint disease requires structured, professional guidance. "
            "Nhealth Physiotherapy brings licensed BPT/MPT physiotherapists directly to your home equipped with portable electrotherapy units (TENS, IFT, Therapeutic Ultrasound, Muscle Stimulators). "
            "We design custom recovery plans for total knee replacement (TKR), hip replacement (THR), stroke paralysis, sciatica, cervical spondylosis, and sports injuries. "
            "Each 45-60 minute bedside session focuses on pain alleviation, joint range-of-motion expansion, balance retraining, and muscle strengthening."
        ),
        "clinical_scope": [
            "Post-Surgical Rehab: Total Knee & Hip Replacement (TKR/THR)",
            "Neurological Rehab: Stroke Hemiplegia, Parkinson's & Bell's Palsy",
            "Spine & Back Care: Sciatica, Slip Disc, Cervical & Lumbar Spondylosis",
            "Joint & Arthritis Care: Frozen Shoulder, Osteoarthritis Knee, Rheumatoid Pain",
            "Sports Injury Rehab: Ligament Tears (ACL/MCL), Ankle Sprains, Tendonitis",
            "Geriatric Fall Prevention & Gait Balance Training"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Initial Clinical Evaluation",
                "desc": "A senior physiotherapist evaluates joint angles, muscle strength, pain triggers, and surgical discharge instructions."
            },
            {
                "step": "2",
                "title": "Personalized Home Therapy Protocol",
                "desc": "Daily 45-60 minute sessions combining electrotherapy, manual mobilization, stretching, and progressive resistance training."
            },
            {
                "step": "3",
                "title": "Objective Milestone Tracking",
                "desc": "Track progress weekly with measurable improvements in walking distance, joint flexion degrees, and pain reduction."
            }
        ],
        "what_included": [
            "Licensed BPT / MPT Physiotherapist Home Visit",
            "Comprehensive Musculoskeletal & Neurological Physical Assessment",
            "Portable Electrotherapy (TENS, IFT, Ultrasound, Heat Therapy)",
            "Manual Joint Mobilization & Deep Tissue Therapy",
            "Customized Home Exercise Protocol Chart"
        ],
        "benefits": [
            "Zero Painful Travel in Auto-Rickshaws or Cars Post Joint Surgery",
            "1-on-1 Dedicated Therapist Focus (Unlike Crowded Hospital Clinics)",
            "Ergonomic Evaluation of Patient's Actual Home Bed, Chairs, and Stairs",
            "Measurable Recovery Benchmarks Within 7 to 14 Days"
        ],
        "pricing_info": "Individual sessions starting from ₹499/session. Discounted 10-session and 20-session recovery packages available.",
        "faqs": [
            {
                "q": "How soon after knee replacement surgery should home physiotherapy start?",
                "a": "Home physiotherapy typically starts 24 to 48 hours after hospital discharge, strictly following the operating orthopedic surgeon's recovery protocol."
            },
            {
                "q": "Do therapists bring machines to home?",
                "a": "Yes. Our therapists carry portable electrotherapy units (TENS, IFT, Ultrasound), resistance bands, and therapeutic equipment for a complete clinical session."
            },
            {
                "q": "How many sessions are typically required for back pain or sciatica?",
                "a": "Most acute back pain patients experience significant relief within 5 to 7 sessions of targeted mobilization and therapeutic core strengthening."
            }
        ],
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
        "slug": "dental-care",
        "title": "Dental Care & Oral Health",
        "category": "Doctor Consultation",
        "filter_cat": "doctor",
        "icon": "tooth",
        "emoji": "🦷",
        "color": "#0284c7",
        "bg_tint": "rgba(2, 132, 199, 0.12)",
        "badge": "Oral Health",
        "hero_image": "images/services/hero/dental-care.jpg",
        "art_image": "images/services/srv_dental_care.png",
        "tagline": "In-Home Dental Scaling, Denture Fitting & Senior Oral Healthcare",
        "description": "Comprehensive dental consultations, portable dental hygiene scaling, painless cavity fillings, dentures, and priority appointments with top dentists.",
        "detailed_overview": (
            "Oral health is deeply connected to cardiac health and overall wellness, yet visiting a dental clinic is often daunting for elderly and immobile patients. "
            "Nhealth Dental Care provides portable oral health consultations, ultrasonic tartar scaling, cavity assessments, and denture adjustments in your home. "
            "Using portable dental equipment, our dental surgeons perform preventive cleanings, assess tooth decay, relieve gum pain, and arrange specialized clinic treatments when complex surgery is required."
        ),
        "clinical_scope": [
            "Comprehensive Oral Physical Examination & Cavity Check",
            "Portable Ultrasonic Dental Scaling & Plaque Polishing",
            "Geriatric Complete & Partial Denture Adjustments and Relining",
            "Toothache Relief, Emergency Dental Prescriptions & Pulpitis Care",
            "Pediatric Fluoride Application & Cavity Prevention Advice",
            "Oral Cancer Screening & Chronic Tobacco Lesion Inspection"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Book Dental Checkup",
                "desc": "Select Home Dental Consultation or Tartar Scaling and enter your location."
            },
            {
                "step": "2",
                "title": "Dentist Arrives with Portable Dental Kit",
                "desc": "A qualified BDS/MDS dentist arrives with sanitized portable instruments, ultrasonic scaler, and oral illumination."
            },
            {
                "step": "3",
                "title": "Bedside Treatment & Denture Care",
                "desc": "The dentist performs ultrasonic scaling, denture corrections, and prescribes necessary medications."
            }
        ],
        "what_included": [
            "Complete Bedside Dental Consultation by Qualified Dental Surgeon",
            "Ultrasonic Teeth Cleaning & Stain Removal",
            "Denture Fit Assessment & Pressure Relief Adjustment",
            "Oral Hygiene Prescription & Medication Guide",
            "Referral & Priority Queue for Advanced Maxillofacial Procedures"
        ],
        "benefits": [
            "Ideal for Elderly Parents Who Cannot Climb Clinic Stairs",
            "Painless, Hygienic Bedside Ultrasonic Scaling",
            "Sterilized Autoclaved Dental Kits with Zero Cross-Contamination",
            "Convenient Family Dental Screening Packages"
        ],
        "pricing_info": "Dental home consultation at ₹499. Ultrasonic scaling packages starting at ₹999.",
        "faqs": [
            {
                "q": "Can dental cleaning (scaling) really be done at home?",
                "a": "Yes. Our dentists use portable ultrasonic dental scalers with independent water reservoirs that perform complete professional cleaning in the comfort of your chair."
            },
            {
                "q": "What can be done for loose dentures at home?",
                "a": "The dentist can inspect gum ridges, perform bedside relining, relieve painful pressure spots, or take fresh impressions for custom-molded dentures."
            },
            {
                "q": "Can tooth extractions be performed at home?",
                "a": "Simple loose deciduous or mobile geriatric teeth can be extracted safely at home. Complex surgical extractions are referred to our accredited clinic partners."
            }
        ],
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
        "slug": "ambulance-services-247",
        "title": "24/7 Smart Ambulance & SOS",
        "category": "Emergency & Critical",
        "filter_cat": "emergency",
        "icon": "truck-medical",
        "emoji": "🚑",
        "color": "#dc2626",
        "bg_tint": "rgba(220, 38, 38, 0.12)",
        "badge": "8-Min Avg Dispatch",
        "hero_image": "images/services/hero/ambulance-services-247.jpg",
        "art_image": "images/services/srv_ambulance_247.png",
        "tagline": "Fastest GPS Emergency Dispatch Linking You to ICU Life-Support Ambulances",
        "description": "Emergency GPS dispatch linking you to the nearest Advanced Life Support (ALS), Basic Life Support (BLS), and Neonatal ambulances across Andhra Pradesh.",
        "detailed_overview": (
            "During a medical emergency, every second counts. Nhealth 24/7 Smart Ambulance network uses automated GPS telemetry to dispatch the nearest emergency vehicle "
            "with an average arrival time of just 8 minutes. Our fleet includes Advanced Life Support (ALS) ICU ambulances equipped with multi-parameter cardiac monitors, "
            "ventilators, defibrillators, oxygen cylinders, suction units, and trained emergency paramedics. "
            "While in transit, our paramedic transmits real-time vitals to the receiving hospital's emergency department, ensuring zero waiting time upon hospital arrival."
        ),
        "clinical_scope": [
            "Cardiac Arrest, Chest Pain, Heart Attack & Stroke Protocol",
            "Severe Respiratory Distress & Low Oxygen Saturation Emergency",
            "Road Accidents, Multi-Trauma & Orthopedic Fractures",
            "Inter-Hospital Critical ICU Patient Transfers on Ventilator",
            "Neonatal & Pediatric Intensive Care Transport (NICU Incubator)",
            "Scheduled Non-Emergency Stretcher Transport for Dialysis / OPD"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "One-Tap SOS or Helpline Call",
                "desc": "Tap the Emergency SOS button or dial our 24/7 toll-free helpline. Your exact GPS coordinates are captured instantly."
            },
            {
                "step": "2",
                "title": "Nearest ALS/BLS Ambulance Dispatched",
                "desc": "The closest ambulance is dispatched immediately with live route tracking sent to the patient's phone."
            },
            {
                "step": "3",
                "title": "Paramedic Care & Hospital Pre-Alert",
                "desc": "Paramedics stabilize the patient with oxygen and vitals monitoring while pre-booking an emergency ICU bed at the destination hospital."
            }
        ],
        "what_included": [
            "Nearest GPS-Tracked Ambulance Dispatch (ALS or BLS)",
            "Trained Emergency Paramedics & Driver Protocol",
            "Continuous High-Flow Oxygen & Cardiac Monitor Telemetry",
            "Onboard Ventilator & Automated Defibrillator (ALS Units)",
            "Emergency Room Pre-Sync with Destination Hospital"
        ],
        "benefits": [
            "Industry-Leading 8-Minute Average Emergency Arrival Time",
            "Direct Tie-ups with 200+ Top Multispecialty Hospital ERs",
            "Clean, Sanitized, Air-Suspension Vehicles for Smooth Transit",
            "Transparent Distance-Based Metering with Zero Price Surges"
        ],
        "pricing_info": "Standard emergency dispatch starts at ₹999 (BLS) and ₹1,999 (ALS ICU with Ventilator & Paramedic).",
        "faqs": [
            {
                "q": "What is the difference between BLS and ALS ambulances?",
                "a": "Basic Life Support (BLS) provides oxygen, stretcher, and basic first aid for stable patients. Advanced Life Support (ALS) is a mobile ICU with ventilator, defibrillator, cardiac monitor, and trained paramedic for critical cases."
            },
            {
                "q": "Can I choose which hospital the ambulance transports the patient to?",
                "a": "Yes. You have full freedom to choose your preferred hospital, or our dispatch coordinator can recommend the nearest available emergency room."
            },
            {
                "q": "Is the ambulance tracking link shareable with family members?",
                "a": "Yes. A real-time live GPS tracking link is immediately sent via SMS and WhatsApp to all registered emergency contacts."
            }
        ],
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
        "slug": "blood-bank",
        "title": "Blood Bank & Support",
        "category": "Emergency & Critical",
        "filter_cat": "emergency",
        "icon": "droplet",
        "emoji": "🩸",
        "color": "#b91c1c",
        "bg_tint": "rgba(185, 28, 28, 0.12)",
        "badge": "24/7 Live Network",
        "hero_image": "images/services/hero/blood-bank.jpg",
        "art_image": "images/services/srv_blood_bank.png",
        "tagline": "Instant Blood Group Availability, Safe Component Transit & Donor Match",
        "description": "Rapid 24/7 blood group availability check, emergency voluntary donor coordination, and safe blood component delivery (PRBC, Platelets, FFP).",
        "detailed_overview": (
            "During critical surgeries, dengue epidemics, trauma resuscitation, or cancer therapy, finding safe matching blood units quickly can save a life. "
            "Nhealth Blood Bank Support provides real-time access to live blood stock inventories across licensed government and private blood banks in Andhra Pradesh. "
            "We coordinate immediate cross-matching, reserve blood components (Packed Red Blood Cells, Single Donor Platelets (SDP), Random Donor Platelets (RDP), Fresh Frozen Plasma (FFP)), "
            "and dispatch them via temperature-monitored refrigerated transit boxes to your hospital operating theatre or bedside."
        ),
        "clinical_scope": [
            "All Blood Group Units: A+, A-, B+, B-, O+, O-, AB+, AB-",
            "Rare Blood Group Sourcing: Bombay Blood Group, Rh-Negative Units",
            "Single Donor Platelets (SDP) for Critical Dengue Thrombocytopenia",
            "Packed Red Blood Cells (PRBC) for Severe Anemia & Surgical Loss",
            "Fresh Frozen Plasma (FFP) & Cryoprecipitate for Coagulation Disorders",
            "Voluntary Blood Donor Emergency Network Mobilization"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Submit Blood Requirement",
                "desc": "Enter the required blood group, component type (PRBC, Platelets, Plasma), hospital name, and requisition slip."
            },
            {
                "step": "2",
                "title": "Live Stock Check & Cross-Matching",
                "desc": "Our 24/7 coordinators locate available screened units at verified blood banks or mobilize voluntary donors."
            },
            {
                "step": "3",
                "title": "Cold-Box Hospital Delivery",
                "desc": "Screened, cross-matched units are transported in certified cold-chain boxes directly to the hospital blood bank."
            }
        ],
        "what_included": [
            "Real-Time Stock Query Across 50+ Certified Blood Banks",
            "100% Screened Units (Tested for HIV, Hepatitis B/C, Malaria, Syphilis)",
            "Temperature-Controlled Cold-Chain Transit Box Delivery",
            "Emergency Donor Mobilization for Rare Blood Types",
            "24/7 Dedicated Blood Coordinator Helpline"
        ],
        "benefits": [
            "Saves Precious Hours Searching from One Blood Bank to Another",
            "Zero Contamination Risk with Certified Nucleic Acid Tested (NAT) Blood",
            "Transparent Government-Approved Component Processing Charges",
            "Dedicated Coordination with Hospital Transfusion Departments"
        ],
        "pricing_info": "Free coordination and stock lookup. Blood component processing charges strictly follow National Blood Transfusion Council (NBTC) guidelines.",
        "faqs": [
            {
                "q": "How quickly can blood units be delivered to a hospital?",
                "a": "Once cross-matching is verified with the patient's blood sample, delivery is completed within 45 to 90 minutes via cold-chain transit."
            },
            {
                "q": "Is replacement blood donation mandatory?",
                "a": "While voluntary replacement donations are encouraged to sustain regional reserves, our team assists in releasing emergency units even when immediate donors are unavailable."
            },
            {
                "q": "How do you verify the safety of the blood units?",
                "a": "Every blood component sourced through our network is mandatory-screened for HIV I & II, Hepatitis B & C, Syphilis, and Malaria via accredited ELISA / NAT testing."
            }
        ],
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
        "slug": "diagnostics-imaging",
        "title": "Diagnostics & Advanced Imaging",
        "category": "Diagnostics & Lab",
        "filter_cat": "diagnostics",
        "icon": "circle-nodes",
        "emoji": "📡",
        "color": "#4f46e5",
        "bg_tint": "rgba(79, 70, 229, 0.12)",
        "badge": "MRI / CT / Scans",
        "hero_image": "images/services/hero/diagnostics-imaging.jpg",
        "art_image": "images/services/srv_diagnostics_imaging.png",
        "tagline": "Priority Slots for 1.5T/3T MRI, 128-Slice CT, 2D Echo & PET Scans",
        "description": "Priority scheduling for high-precision 1.5T/3T MRI, 128-slice CT Scans, Ultrasound, 2D Echo, Mammography, and PET Scans with expert radiologist reports.",
        "detailed_overview": (
            "Getting an advanced radiological imaging scan shouldn't involve days of waiting or crowded hospital registration counters. "
            "Nhealth Advanced Imaging provides priority appointments at accredited diagnostic imaging centers with state-of-the-art 1.5T & 3T MRI machines, "
            "128-slice dual-source CT scanners, 4D Ultrasound, Digital Mammography, 2D Echocardiography, and PET-CT oncology scans. "
            "Enjoy discounted institutional pricing, zero waiting time, dedicated on-ground care coordinators at the scan center, "
            "and digital cloud access to high-resolution DICOM scan slices with second-opinion radiologist reports."
        ),
        "clinical_scope": [
            "3 Tesla MRI: Brain, Spine, Knee Joint, Musculoskeletal & Pelvis",
            "128-Slice CT Scans: High-Resolution Chest (HRCT), Abdomen & Angiography",
            "Cardiology Imaging: 2D Echo with Doppler, Treadmill Test (TMT), Holter",
            "Ultrasound & Doppler: Abdominal, Pelvic, Obstetric 4D Scan, Venous Doppler",
            "Women's Health Imaging: Digital Mammography & Bone Mineral Density (DEXA)",
            "Oncology: Whole Body FDG PET-CT Scans for Cancer Staging"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Upload Prescription & Select Scan",
                "desc": "Upload doctor scan prescription. Select your preferred scan center or let our AI match the closest accredited facility."
            },
            {
                "step": "2",
                "title": "Zero-Wait VIP Appointment",
                "desc": "Receive a confirmed priority time slot. Arrive at the scan center where our Care Coordinator assists with check-in."
            },
            {
                "step": "3",
                "title": "Digital Cloud DICOM Access & Report",
                "desc": "Receive original DICOM images on the cloud same-day and expert signed radiologist reports within 6 to 12 hours."
            }
        ],
        "what_included": [
            "Priority VIP Slot Reservation at Accredited Scan Centers",
            "High-Precision 1.5T / 3T MRI or 128-Slice Low-Dose CT",
            "Dedicated On-Ground Patient Care Coordinator Assistance",
            "Digital Cloud Link to Raw DICOM Slices (Shareable with Surgeons)",
            "Institutional Discounted Rates (Up to 30% Below Hospital Walk-in Rates)"
        ],
        "benefits": [
            "No Standing in Long Hospital Registration & Billing Queues",
            "High-Resolution Imaging Ensures Accurate Clinical Diagnosis",
            "Radiologist Second-Opinion Available on Request",
            "Direct Sync with Nhealth Patient Electronic Health Records (EHR)"
        ],
        "pricing_info": "CT Scans start from ₹1,999. MRI Scans starting from ₹3,499 with up to 30% savings compared to hospital tariffs.",
        "faqs": [
            {
                "q": "Will I have to wait in line at the scan center?",
                "a": "No. Nhealth patients receive priority VIP time slots. Our on-ground coordinator manages your registration and escorts you directly to the scan console."
            },
            {
                "q": "How soon will my doctor receive the scan report?",
                "a": "Digital DICOM images are available online within 1 hour of scan completion. The formal signed radiologist diagnostic report is ready within 6 hours."
            },
            {
                "q": "Do I need fasting for an abdomen CT or MRI scan?",
                "a": "Contrast-enhanced scans (CECT/CEMRI) require 4-6 hours of fasting and a recent normal Serum Creatinine lab test. Our team will guide you through all preparation instructions."
            }
        ],
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
        "slug": "home-vaccination",
        "title": "Home Vaccination Service",
        "category": "Preventive & Care Plans",
        "filter_cat": "preventive",
        "icon": "syringe",
        "emoji": "💉",
        "color": "#10b981",
        "bg_tint": "rgba(16, 185, 129, 0.12)",
        "badge": "Cold-Chain Safe",
        "hero_image": "images/services/hero/home-vaccination.jpg",
        "art_image": "images/services/srv_home_vaccination.png",
        "tagline": "WHO-Compliant Cold-Chain Vaccines Administered Safely by Certified Nurses",
        "description": "Certified healthcare nurses deliver and administer WHO-approved cold-chain maintained vaccines safely at your home for infants, children, and adults.",
        "detailed_overview": (
            "Visiting clinics with infants or elderly parents for routine immunizations risks exposure to viral infections in crowded waiting rooms. "
            "Nhealth Home Vaccination brings genuine, WHO-approved vaccines straight to your home. "
            "Vaccines are stored and transported in strict compliance with the Cold-Chain protocol (2°C to 8°C) with digital data-logger verification. "
            "Our licensed healthcare nurses evaluate the recipient's temperature and medical history, administer the vaccine with gentle, sterile technique, "
            "observe the patient post-injection for 15 minutes, and issue a verified digital immunization certificate."
        ),
        "clinical_scope": [
            "Complete Childhood Immunization Schedule (BCG, DPT, Polio, MMR, Rotavirus)",
            "Adult Influenza (Flu) Annual Preventive Vaccine",
            "Pneumococcal Vaccine (Prevenar-13 / Pneumovax-23) for Seniors & Diabetics",
            "Hepatitis A and Hepatitis B Immunization Series",
            "HPV (Cervical Cancer) Vaccination for Girls & Young Women",
            "Typhoid, Tetanus (Tdap), and Shingles (Herpes Zoster) Vaccines"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Select Vaccine",
                "desc": "Choose your required pediatric or adult vaccine, or upload your child's vaccination card for schedule verification."
            },
            {
                "step": "2",
                "title": "Cold-Chain Doorstep Delivery",
                "desc": "A certified nurse arrives with the vaccine in a temperature-monitored carrier box showing verified 2°C-8°C readings."
            },
            {
                "step": "3",
                "title": "Gentle Administration & Digital Certificate",
                "desc": "Nurse checks vitals, administers the injection, monitors for 15 minutes, and issues an updated immunization record."
            }
        ],
        "what_included": [
            "100% Genuine WHO-Approved Vaccine with Batch & Expiry Verification",
            "Verified Cold-Chain Temperature Box Transport (2°C to 8°C)",
            "Administration by Certified Registered Pediatric/General Nurse",
            "15-Minute Post-Vaccination Observation & Vitals Check",
            "Digital Immunization Certificate & Next-Dose Reminders"
        ],
        "benefits": [
            "Zero Waiting Room Exposure to Sick Patients for Fragile Infants & Elders",
            "Comfortable, Tear-Free In-Home Environment for Children",
            "Digital Temperature Log Verifies Vaccine Potency Prior to Injection",
            "Automated Reminders Ensure Never Missing a Scheduled Booster Dose"
        ],
        "pricing_info": "Vaccines priced at transparent MRP with no hidden markups. Nominal in-home administration charge of ₹249.",
        "faqs": [
            {
                "q": "How can I be sure the vaccine was stored at the correct temperature?",
                "a": "Our cold boxes feature an external digital thermometer display. The nurse shows you the verified 2°C to 8°C temperature reading and the intact vaccine vial monitor (VVM) before opening the vial."
            },
            {
                "q": "Do you follow the official Indian Academy of Pediatrics (IAP) schedule?",
                "a": "Yes. Our pediatric vaccination protocols strictly mirror the guidelines of the Indian Academy of Pediatrics (IAP) and WHO."
            },
            {
                "q": "Which vaccines are recommended for senior citizens above 60?",
                "a": "Seniors and chronic disease patients are strongly advised to take the Annual Flu vaccine and the Pneumococcal pneumonia vaccine to prevent life-threatening chest infections."
            }
        ],
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
        "slug": "health-checkups",
        "title": "Full Body Preventive Screening",
        "category": "Preventive & Care Plans",
        "filter_cat": "preventive",
        "icon": "heart-pulse",
        "emoji": "🛡️",
        "color": "#ca8a04",
        "bg_tint": "rgba(202, 138, 4, 0.12)",
        "badge": "85+ Parameters",
        "hero_image": "images/services/hero/health-checkups.png",
        "art_image": "images/services/srv_health_checkups.png",
        "tagline": "Comprehensive 85+ Vital Parameters Screened at Home with Free MD Doctor Review",
        "description": "Comprehensive annual preventive health packages covering 85+ parameters including Cardiac Risk, Liver, Kidney, Thyroid, Vitamin D/B12, and Diabetes.",
        "detailed_overview": (
            "Lifestyle conditions such as diabetes, hypertension, dyslipidemia, and fatty liver often develop silently without overt symptoms. "
            "Nhealth Full Body Preventive Screening packages analyze 85+ critical blood and urine biomarkers from the comfort of your home. "
            "Our master packages evaluate cardiac risk, liver function, renal efficiency, thyroid balance, bone health (Vitamin D3), energy metabolism (Vitamin B12), "
            "blood sugar trends (HbA1c), and complete hemogram. Once your smart digital report is generated, an experienced MD physician conducts a teleconsultation "
            "to explain your results and recommend actionable lifestyle and dietary modifications."
        ),
        "clinical_scope": [
            "Cardiac Risk Profile: Lipid Profile (Cholesterol, Triglycerides, HDL, LDL, VLDL)",
            "Diabetes Index: Fasting Blood Sugar, Average 3-Month Glucose (HbA1c)",
            "Liver Function (LFT): Bilirubin, SGOT/AST, SGPT/ALT, Alkaline Phosphatase",
            "Kidney Function (KFT): Serum Creatinine, Blood Urea Nitrogen (BUN), Uric Acid",
            "Thyroid Panel: T3, T4, and Ultra-Sensitive TSH",
            "Deficiency Markers: Vitamin D3 (25-OH) & Vitamin B12",
            "Complete Hemogram: Hemoglobin, RBC, Total WBC, Platelets, ESR"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Select Master Health Package",
                "desc": "Select the Full Body Preventive Checkup or Senior Citizen Profile and choose a morning home fasting slot."
            },
            {
                "step": "2",
                "title": "Phlebotomist Home Sample Draw",
                "desc": "Certified phlebotomist collects blood and urine samples safely at your residence with barcoded vacutainer tubes."
            },
            {
                "step": "3",
                "title": "Smart Report & Free MD Review",
                "desc": "Receive your 85-parameter smart PDF report within 6 hours, followed by a free teleconsultation with an MD physician."
            }
        ],
        "what_included": [
            "85+ Comprehensive Vital Biochemical Parameters Tested",
            "In-Home Blood & Urine Sample Collection with Sterile Vacutainers",
            "NABL / CAP Accredited Pathology Automated Testing",
            "Color-Coded Smart Health Risk Assessment Report",
            "Free MD Physician Teleconsultation & Diet Counseling"
        ],
        "benefits": [
            "Early Detection of Silent Cardiac, Liver, and Metabolic Diseases",
            "Save Over 60% Compared to Walk-in Hospital Health Checkup Tariffs",
            "Year-on-Year Trend Analysis to Monitor Biomarker Improvements",
            "Family Master Packages Available Covering Parents and Children"
        ],
        "pricing_info": "Complete 85-parameter preventive health package starting at ₹1,499 (Valued at ₹4,500 at hospital labs).",
        "faqs": [
            {
                "q": "How should I prepare for the full-body screening?",
                "a": "Fast for 10-12 hours overnight. Drinking plain water is allowed and encouraged. Avoid heavy alcohol or strenuous workouts the evening prior."
            },
            {
                "q": "How does the free doctor consultation work?",
                "a": "Once your lab report is ready, you will receive an SMS and WhatsApp link to choose your preferred time for a 1-on-1 video/phone call with an MD physician."
            },
            {
                "q": "Can multiple family members get tested on the same visit?",
                "a": "Yes! Our phlebotomist can collect samples for the entire family during a single morning visit with additional multi-member package discounts."
            }
        ],
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
        "slug": "care-programmes",
        "title": "Chronic Disease Care Programmes",
        "category": "Preventive & Care Plans",
        "filter_cat": "preventive",
        "icon": "user-shield",
        "emoji": "📋",
        "color": "#7c3aed",
        "bg_tint": "rgba(124, 58, 237, 0.12)",
        "badge": "360° Management",
        "hero_image": "images/services/hero/care-programmes.png",
        "art_image": "images/services/srv_care_programmes.png",
        "tagline": "360° Continuous Management for Diabetes, Hypertension & Cardiac Wellness",
        "description": "Tailored 360° continuous disease management programs for Diabetes, Hypertension, Cardiac Health, Asthma, COPD, and Thyroid wellness.",
        "detailed_overview": (
            "Managing chronic conditions like Type 2 Diabetes, Hypertension, and Coronary Artery Disease cannot be resolved with sporadic, quarterly clinic visits. "
            "Nhealth Chronic Care Programmes provide continuous 360° disease management. "
            "Subscribers are assigned a personal Care Manager, monthly doctor consultations, quarterly in-home lab tests (HbA1c, Lipids, Creatinine), "
            "automated doorstep medicine delivery with 20% savings, and personalized dietary guidance. "
            "With continuous tracking of your blood sugar and BP readings, our team detects adverse trends early to prevent long-term microvascular and cardiac complications."
        ),
        "clinical_scope": [
            "Diabetes Mellitus (Type 2): HbA1c Reduction & Neuropathy Prevention",
            "Hypertension & Cardiovascular Health: BP Stabilization & Stroke Prevention",
            "Respiratory Care: Asthma & Chronic Obstructive Pulmonary Disease (COPD)",
            "Thyroid Disorders: Hypothyroidism TSH Normalization",
            "Chronic Kidney Disease (CKD): Early Stage eGFR & Creatinine Monitoring",
            "Weight & Metabolic Syndrome Reversal Programs"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Enroll & Baseline Assessment",
                "desc": "Enroll in your tailored program (Diabetes, Heart, or Dual Care). We conduct baseline in-home lab tests and doctor review."
            },
            {
                "step": "2",
                "title": "Personal Care Manager Assigned",
                "desc": "Your dedicated Care Manager coordinates regular vitals logging, monthly doctor check-ins, and nutritionist meal plans."
            },
            {
                "step": "3",
                "title": "Automated Refills & Quarterly Labs",
                "desc": "Enjoy automatic discounted doorstep medicine delivery and quarterly in-home lab screening with ongoing progress reviews."
            }
        ],
        "what_included": [
            "Dedicated Personal Health Manager & Tele-Nurse Support",
            "Monthly 1-on-1 Specialist Doctor Follow-Up Consultations",
            "Quarterly In-Home Blood Tests (HbA1c, Lipid, KFT)",
            "Automated Monthly Medicine Delivery with Flat 20% Discount",
            "Customized Clinical Nutrition & Exercise Regimen"
        ],
        "benefits": [
            "Proven Clinical Reduction in HbA1c Levels within 90 Days",
            "Prevents Sudden Hospitalization for Diabetic Coma or BP Crises",
            "Zero Coordination Stress: Medicines and Tests Handled Automatically",
            "24/7 Dedicated WhatsApp Emergency Health Assistance"
        ],
        "pricing_info": "Annual care subscriptions starting at ₹999/month. Includes quarterly labs, monthly doctor consults, and priority medicine delivery.",
        "faqs": [
            {
                "q": "Can this program help reduce my diabetes medication dosage?",
                "a": "Yes! Through disciplined dietary modification, structured exercise, and continuous physician monitoring, many of our patients successfully lower their HbA1c and reduce medication dependence."
            },
            {
                "q": "Are the lab tests included in the monthly subscription fee?",
                "a": "Yes. Quarterly home lab tests (HbA1c, Fasting Sugar, Lipid Profile, Creatinine) are included with zero out-of-pocket charges."
            },
            {
                "q": "How does the Care Manager assist me daily?",
                "a": "Your Care Manager tracks your home glucometer and BP readings, reminds you of medication times, answers questions on WhatsApp, and schedules doctor consultations."
            }
        ],
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
        "slug": "mental-health",
        "title": "Mental Health & Counseling",
        "category": "Rehabilitation & Therapy",
        "filter_cat": "rehab",
        "icon": "brain",
        "emoji": "🧠",
        "color": "#9333ea",
        "bg_tint": "rgba(147, 51, 234, 0.12)",
        "badge": "100% Confidential",
        "hero_image": "images/services/hero/mental-health.png",
        "art_image": "images/services/srv_mental_health.png",
        "tagline": "Private, Empathetic 1-on-1 Therapy with Licensed Psychologists & Psychiatrists",
        "description": "Confidential 1-on-1 online therapy and psychiatric counseling with licensed clinical psychologists for anxiety, depression, stress, burnout, and wellness.",
        "detailed_overview": (
            "Mental wellness is just as vital as physical health. Nhealth Mental Health provides private, judgment-free clinical therapy and psychiatric support. "
            "Connect with licensed clinical psychologists (M.Phil / RCI registered) and MD Psychiatrists via encrypted video or audio sessions from the privacy of your home. "
            "Whether you are dealing with chronic anxiety, clinical depression, work burnout, relationship stress, grief, sleep disorders, or panic attacks, "
            "our therapists utilize evidence-based modalities including Cognitive Behavioral Therapy (CBT), Mindfulness-Based Stress Reduction, and positive psychotherapy."
        ),
        "clinical_scope": [
            "Anxiety Disorders, Social Phobia & Panic Attacks",
            "Clinical Depression, Low Mood & Chronic Fatigue",
            "Workplace Stress, Professional Burnout & Academic Pressure",
            "Relationship, Marriage & Family Dynamics Counseling",
            "Insomnia, Sleep Disturbances & Circadian Rhythm Irregularities",
            "Grief, Bereavement & Trauma Recovery (PTSD)"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Confidential Assessment",
                "desc": "Answer a short, confidential wellness questionnaire to help us match you with the right specialist psychologist."
            },
            {
                "step": "2",
                "title": "Select Therapist & Session Slot",
                "desc": "Browse verified therapist profiles, clinical specializations, languages spoken, and book a convenient evening or weekend slot."
            },
            {
                "step": "3",
                "title": "1-on-1 Encrypted Therapy Session",
                "desc": "Join a 45-minute private, encrypted video or audio room. Receive personalized coping strategies and mental health exercises."
            }
        ],
        "what_included": [
            "45-Minute 1-on-1 Private Consultation with RCI-Licensed Psychologist",
            "100% End-to-End Encrypted Session with Zero Identity Disclosure",
            "Personalized Cognitive Behavioral Therapy (CBT) Worksheets",
            "Prescription Support from MD Psychiatrists when Clinically Indicated",
            "Free Follow-up Messaging with Therapist Between Sessions"
        ],
        "benefits": [
            "Complete Stigma-Free Confidentiality in the Comfort of Your Private Room",
            "Flexible Evening & Weekend Timings to Accommodate Busy Work Schedules",
            "Multi-lingual Therapists: Telugu, English, Hindi & Tamil",
            "Evidence-Based Measurable Improvements in Mood and Sleep Quality"
        ],
        "pricing_info": "Individual 45-minute therapy sessions start at ₹699. Discounted multi-session packages (4 and 8 sessions) available.",
        "faqs": [
            {
                "q": "Is my consultation strictly confidential?",
                "a": "Yes, absolutely. All sessions are 100% confidential and encrypted. No session recordings are ever stored, and patient identity is strictly safeguarded under medical privacy laws."
            },
            {
                "q": "What is the difference between a Psychologist and a Psychiatrist?",
                "a": "Clinical psychologists provide psychological counseling, talk therapy, and CBT without medications. Psychiatrists are medical doctors (MD) who diagnose complex conditions and prescribe medications when necessary."
            },
            {
                "q": "Can I consult via audio-only if I don't want to turn on my video camera?",
                "a": "Yes. You have full freedom to choose audio-only calls or video consultation according to your comfort level."
            }
        ],
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
        "slug": "premium-opd",
        "title": "Premium OPD & Hospital Assistance",
        "category": "Preventive & Care Plans",
        "filter_cat": "preventive",
        "icon": "crown",
        "emoji": "👑",
        "color": "#d97706",
        "bg_tint": "rgba(217, 119, 6, 0.12)",
        "badge": "VIP Priority",
        "hero_image": "images/services/hero/premium-opd.png",
        "art_image": "images/services/srv_premium_opd.png",
        "tagline": "VIP Zero-Queue Hospital Access, On-Ground Care Buddy & Deep Discounts",
        "description": "Exclusive healthcare memberships offering unlimited doctor consultations, hospital OPD priority queues, procedure coordination, and deep discounts.",
        "detailed_overview": (
            "Navigating a large multispecialty hospital can be confusing and stressful—standing in billing lines, waiting hours outside doctor chambers, "
            "and coordinating diagnostic labs. Nhealth Premium OPD & Hospital Assistance provides VIP healthcare concierge support. "
            "Members are met at the hospital entrance by a dedicated on-ground Care Buddy who manages registration, holds priority doctor slots, "
            "fast-tracks diagnostic tests, and negotiates up to 30% discounts on surgeries, room rents, and pharmacy bills across 100+ partner hospitals in Andhra Pradesh."
        ),
        "clinical_scope": [
            "Zero Waiting Time in Top Hospital OPD Consultation Queues",
            "Dedicated On-Ground Hospital Care Buddy for Senior Citizens & Families",
            "Planned Surgery Coordination & Cashless TPA Health Insurance Assistance",
            "Priority Admission to Private & Deluxe Hospital Rooms",
            "Up to 30% Institutional Discounts on Diagnostics, Imaging & Pharmacy",
            "Full Family Medical Record Digitization & Hospital Liaison"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Activate Membership & Request Visit",
                "desc": "Choose your hospital and specialist, or let our medical concierge recommend the top surgeon for your specific procedure."
            },
            {
                "step": "2",
                "title": "Care Buddy Greets You at Entrance",
                "desc": "Your dedicated Care Buddy meets you at the hospital porch with a wheelchair if needed, handling all billing and tokens."
            },
            {
                "step": "3",
                "title": "VIP Fast-Track Care & Discounted Billing",
                "desc": "Bypass regular queues, complete your consultation, and enjoy pre-negotiated corporate discounts on all hospital bills."
            }
        ],
        "what_included": [
            "Personal On-Ground Hospital Care Buddy Assistance for Every Visit",
            "Priority Queue Token at 100+ Partner Hospitals",
            "Up to 30% Discount on In-Patient Surgeries, Diagnostics & Scans",
            "Comprehensive Health Insurance Pre-Authorization & Cashless TPA Support",
            "Free Post-Discharge Follow-up Teleconsultation"
        ],
        "benefits": [
            "Eliminates All Waiting Stress and Administrative Confusion in Hospitals",
            "Significant Financial Savings on Major Surgical & Diagnostic Procedures",
            "Invaluable for Senior Citizens Visiting Hospitals Without Adult Children",
            "Single Point of Contact for All Hospital Admissions Across Andhra Pradesh"
        ],
        "pricing_info": "Annual family membership at ₹1,999/year covering up to 4 family members with unlimited hospital visit assistance.",
        "faqs": [
            {
                "q": "Which hospitals in Andhra Pradesh are covered under Premium OPD?",
                "a": "We have formal partnerships with leading tertiary care and superspecialty hospitals across Vijayawada, Guntur, Visakhapatnam, Tirupati, Rajahmundry, and Kurnool."
            },
            {
                "q": "How does the Care Buddy help senior citizens?",
                "a": "The Care Buddy meets the senior at the hospital entrance, arranges a wheelchair if needed, guides them to the doctor's cabin, holds medical files, collects medicines from the pharmacy, and escorts them safely back to their vehicle."
            },
            {
                "q": "Does the membership cover cashless health insurance claims?",
                "a": "Yes! Our dedicated TPA desk helps expedite cashless approvals and coordinates all required medical documents directly with your insurance provider."
            }
        ],
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
        "slug": "health-support-rider",
        "title": "Health Support Rider",
        "category": "Emergency & Critical",
        "filter_cat": "emergency",
        "icon": "motorcycle",
        "emoji": "🛵",
        "color": "#0baaa2",
        "bg_tint": "rgba(11, 170, 162, 0.12)",
        "badge": "Pick • Support • Drop",
        "hero_image": "images/services/hero/health-support-rider.jpg",
        "art_image": "images/health_support_rider.png",
        "tagline": "Trusted Hospital Pick, Escort, Support & Drop for Patients and Seniors",
        "description": "Dedicated healthcare riders providing trusted patient pick & drop, hospital OPD accompaniment, procedure assistance, and doorstep medicine & report delivery.",
        "detailed_overview": (
            "Nhealth Health Support Rider is India's first specialized healthcare transit and accompaniment fleet. "
            "Unlike generic commercial ride-hailing apps, our Health Support Riders are trained in patient care, senior assistance, basic first aid, and hospital navigation. "
            "A rider arrives at your doorstep, assists the patient onto the vehicle or escorts them, safely drives them to the hospital or diagnostic clinic, "
            "stays with the patient throughout OPD queues, blood draws, or physiotherapy sessions, and drops them back safely at home. "
            "With real-time GPS tracking and pre-paid zero-cash billing, anxious family members can monitor the journey live from anywhere."
        ),
        "clinical_scope": [
            "Doorstep Pick & Hospital OPD Accompaniment for Senior Citizens",
            "Dialysis & Chemotherapy Scheduled Twice/Thrice-Weekly Transit",
            "Physiotherapy & Eye Clinic Routine Follow-up Accompaniment",
            "Express Doorstep Diagnostic Lab Sample & Report Delivery",
            "Emergency Doorstep Prescription Medicine Pickup & Delivery",
            "Full-Day Patient Companion for Diagnostic Scans & Checkups"
        ],
        "how_it_works": [
            {
                "step": "1",
                "title": "Enter Pickup & Hospital Drop",
                "desc": "Enter pickup address and target hospital on our live Rapido-style interactive map. Fare and ETA calculate in real-time."
            },
            {
                "step": "2",
                "title": "Pay-First Online & Get Tax Invoice",
                "desc": "Complete online payment via UPI QR or card. An instant official tax invoice is generated with a 4-digit start OTP."
            },
            {
                "step": "3",
                "title": "Rider Arrives & Accompanies Patient",
                "desc": "Verified rider arrives with a sanitized helmet. Share the OTP to begin the ride with live GPS family tracking."
            }
        ],
        "what_included": [
            "Trained, Background-Verified & KYC Cleared Healthcare Rider",
            "Safe Hospital Pick-up, Accompaniment, and Return Drop-off",
            "4-Digit OTP Verified Ride Start for Patient Safety",
            "Real-Time Live Journey Tracking via Leaflet OSRM Maps",
            "Official Automated Tax Invoice Issued Immediately upon Booking"
        ],
        "benefits": [
            "Trained in Senior Citizen Patience and Gentle Transit (Unlike Taxis)",
            "Rider Waits and Assists Patient in Hospital Waiting Areas",
            "Zero Cash Handling: 100% Pre-Paid Online Security",
            "Live GPS Tracking Shared with Children & Relatives"
        ],
        "pricing_info": "Standard fare starts at ₹120 for the first 2.5 km, plus nominal per-km distance rates. Transparent billing with automated tax invoices.",
        "faqs": [
            {
                "q": "How is a Health Support Rider different from regular ride-hailing?",
                "a": "Our riders are police-verified, KYC-checked healthcare companions trained to assist frail or elderly patients, help them walk safely, hold medical files, and stay throughout the hospital visit."
            },
            {
                "q": "What is the cancellation policy for rider booking?",
                "a": "Once booked and paid, the service cannot be cancelled or refunded, and the payment is valid for that calendar day."
            },
            {
                "q": "Can family members track the journey in real-time?",
                "a": "Yes! The live GPS tracking screen shows exact motorcycle coordinates, route geometry, heading, and live ETA throughout the trip."
            }
        ],
        "features": [
            "Safe Hospital Pick, Escort, Support & Drop-off",
            "Full-Day Dedicated Patient Companion for OPDs & Tests",
            "Express Doorstep Medicine & Diagnostic Report Delivery",
            "Real-Time Live Journey Tracking for Anxious Families"
        ],
        "action_label": "Book Health Rider",
        "action_fn": "window.location.href='/rider/book'"
    }
]

# 🏥 Nhealth — Healthcare at Home

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/Flask-2.3%2B-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-Neon%20PostgreSQL%20%2B%20JSON%20Fallback-00e599.svg)](https://neon.tech/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20%28Backend%20%2B%20Frontend%29-orange.svg)](#-codebase-architecture)

**Nhealth** is an enterprise-grade digital healthcare platform and home medical marketplace that connects patients, board-certified doctors, diagnostic pathology laboratories, certified pharmacies, and a dedicated Health Support Rider fleet under a single unified ecosystem across Andhra Pradesh and all of Bharat.

---

## 📋 Table of Contents
1. [Overview & Vision](#-overview--vision)
2. [Codebase Architecture (Modular Structure)](#-codebase-architecture)
3. [Portals & Dashboards](#-portals--dashboards)
4. [Comprehensive 19 Healthcare Services](#-comprehensive-19-healthcare-services)
5. [Health Support Rider & Rapido-Style Booking](#-health-support-rider--rapido-style-booking)
6. [Authentication, Security & KYC](#-authentication-security--kyc)
7. [Official Demo Credentials](#-official-demo-credentials)
8. [Database Layer & Resilience](#-database-layer--resilience)
9. [Complete API Reference](#-complete-api-reference)
10. [Local Development Setup](#-local-development-setup)
11. [Running Tests](#-running-tests)
12. [Production Deployment](#-production-deployment)
13. [License](#-license)

---

## 🌟 Overview & Vision

Nhealth addresses the fragmentation in doorstep medical delivery by offering:
- **100vh Desktop Single-Screen Experience**: Calligraphy accents, interactive Andhra Pradesh coverage map, dynamic service carousels, and live operational stats.
- **Native-Like Mobile Experience**: Dedicated mobile art backdrop, AI symptom search pill, 4-column service grid, quick emergency actions, and bottom navigation.
- **Telemedicine Virtual Clinic**: Real-time encrypted consultation room featuring live vitals telemetry (Pulse, SpO2, Blood Pressure), synchronized doctor chat, and digital e-prescription generation dispatched directly to WhatsApp.
- **Health Support Rider Fleet**: Trusted accompaniment for senior citizens and mobility-challenged patients traveling to hospitals for OPDs, diagnostics, and procedures.
- **Hybrid Data Resilience**: High-performance Neon Serverless PostgreSQL with zero-downtime automatic fallback to local JSON storage.

---

## 🏗️ Codebase Architecture

The project is structured with strict separation of concerns into dedicated `backend/` and `frontend/` folders:

```
d:/nhealth final/
│
├── backend/                             # 🧠 ALL Backend Code (Modularized)
│   ├── __init__.py                      # Flask App Factory (create_app), custom JSON serializer, ChoiceLoader
│   ├── config.py                        # App Configuration (Secret keys, cookies, cache policies)
│   │
│   ├── models/                          # Database Access Layer (PostgreSQL + JSON fallback)
│   │   ├── __init__.py                  # Re-exports all models, triggers init_db()
│   │   ├── base.py                      # Neon PostgreSQL pool, helpers, serializers, JSON fallbacks
│   │   ├── users.py                     # User operations (get_all_users, save_user, update_user)
│   │   ├── bookings.py                  # Home healthcare bookings (save_booking, get_all_bookings)
│   │   ├── contacts.py                  # Contact inquiries (save_contact, get_all_contacts)
│   │   ├── trips.py                     # Rider & trip management (10 lifecycle functions)
│   │   └── invoices.py                  # Automated sequential invoice number generator
│   │
│   ├── routes/                          # Modular Flask Route Blueprints
│   │   ├── __init__.py                  # Blueprint registration manager (register_routes)
│   │   ├── pages.py                     # Public pages (/, /contact) & info APIs (/api/services, etc.)
│   │   ├── auth.py                      # Auth pages & APIs (/login, /signup, /logout, /api/auth/*)
│   │   ├── patient.py                   # Patient portal (/patient/dashboard, /rider/book)
│   │   ├── rider.py                     # Rider portal (/rider/dashboard) & cockpit APIs (/api/rider/*)
│   │   ├── doctor.py                    # Doctor teleconsultation suite (/doctor/dashboard)
│   │   ├── pharmacy.py                  # Pharmacy partner portal (/pharmacy/dashboard)
│   │   ├── lab.py                       # Diagnostic lab portal (/lab/dashboard)
│   │   ├── trips.py                     # Trip booking, live tracking & tax invoices (/api/trip/*)
│   │   ├── bookings.py                  # General booking & contact submissions (/api/book, /api/contact)
│   │   └── profile.py                   # Patient profile management (/api/user/profile)
│   │
│   ├── services/                        # Business Logic & Utility Helpers
│   │   ├── __init__.py                  # Services re-export
│   │   ├── auth_helpers.py              # Password verification, rate limiting, patient field normalization
│   │   └── patient_helpers.py           # Session patient resolution
│   │
│   ├── data/                            # Static Catalog Constants
│   │   ├── __init__.py                  # Catalog exports
│   │   ├── services_catalog.py          # 19 comprehensive healthcare services
│   │   ├── locations.py                 # 15 key Andhra Pradesh coverage cities
│   │   └── stats.py                     # Platform trust metrics & stats
│   │
│   └── seeds/                           # Seeding Utilities
│       ├── __init__.py
│       └── demo_accounts.py             # Default demo accounts for testing
│
├── frontend/                            # 🎨 ALL Frontend Assets (Zero UI Changes)
│   ├── templates/                       # Jinja2 Templates Organized by Category
│   │   ├── pages/                       # index.html, contact.html
│   │   ├── auth/                        # login.html, login_lab.html, login_rider.html, signup_*.html
│   │   └── dashboards/                  # patient, doctor, pharmacy, lab, rider, book_rider
│   └── static/                          # Static Assets
│       ├── css/                         # All stylesheets (auth, dashboards, book_rider)
│       ├── js/                          # Client-side scripts (main.js)
│       ├── images/                      # Brand logos, service artwork, banners
│       └── videos/                      # Intro background videos (desktop & mobile)
│
├── data/                                # Local JSON Fallback Storage
│   ├── bookings.json                    # Appointment bookings fallback
│   ├── contacts.json                    # General inquiry messages fallback
│   ├── trips.json                       # Rider trip records fallback
│   └── users.json                       # Registered users fallback
│
├── tests/                               # 🧪 Automated Test Suite
│   ├── conftest.py                      # Test configuration & sys.path setup
│   ├── test_audit_fixes.py              # Rider KYC, 2 contact numbers, Town/Village tests
│   ├── test_payment_invoice_flow.py     # Pay-first flow, tax invoice generation tests
│   └── test_rider_flow.py               # Rider dispatch, acceptance & live tracking tests
│
├── app.py                               # Slim 18-line entry point (`web: gunicorn app:app`)
├── db.py                                # Backward-compatibility facade (`from backend.models import *`)
├── requirements.txt                     # Python dependencies
├── Procfile                             # WSGI production server config
└── .env                                 # Environment secrets (DATABASE_URL, SECRET_KEY)
```

---

## 🖥️ Portals & Dashboards

### 1. Patient Portal & Telemedicine (`/patient/dashboard`)
- **Live Video Consultation**: Connect with general physicians and specialists with video feed, audio controls, and picture-in-picture.
- **Vital Telemetry**: Real-time tracking of Heart Rate, SpO2, Blood Pressure, and Temperature.
- **Digital E-Prescriptions**: Instantly generated prescriptions with medicines, dosages, and direct WhatsApp dispatch.
- **Health Records & History**: Digital access to past appointments, lab test results, and pharmacy orders.
- **Profile Management**: Inline updates for name, phone, blood group, address, age, and date of birth.

### 2. Doctor Teleconsultation Suite (`/doctor/dashboard`)
- **Live Waiting Room**: Real-time queue of incoming patients with symptom tags.
- **Clinical Charting**: Bedside examination notes, diagnosis documentation, and medical history review.
- **Digital Rx Generator**: One-click prescription builder with pre-filled dosages, frequency, and instructions.
- **Vitals Monitor**: Live feed of patient vitals during teleconsultation.

### 3. Pharmacy Partner Portal (`/pharmacy/dashboard`)
- **Order Queue**: Inflow of incoming e-prescriptions and OTC orders.
- **Cold-Chain Verification**: Temperature monitoring for insulin, vaccines, and biologics.
- **2-Hour Express Dispatch**: Delivery partner assignment and route optimization.
- **Refill Tracking**: Chronic medication replenishment reminders for patients.

### 4. Diagnostic Lab Portal (`/lab/dashboard`)
- **Sample Intake**: Barcoded vacutainer sample logging for blood, urine, and pathology.
- **Test Results Entry**: 500+ NABL test parameter inputs with reference range validation.
- **Smart PDF Reports**: Automated verified report generation with QR code validation delivered in under 6 hours.

### 5. Rider Cockpit Dashboard (`/rider/dashboard`)
- **Duty Toggle**: Instant Online / Offline status switch.
- **Live Task Queue**: Incoming accompaniment and transport requests with distance and fare preview.
- **Trip Workflow**: Accept Task ➔ Arrive at Pickup ➔ Verify 4-Digit OTP ➔ In Transit ➔ Complete Trip.
- **12-Hour AM/PM History**: Full audit trail of completed and ended trips.
- **Online Payment Verified**: Tagged with zero cash handling policy.

---

## 🩺 Comprehensive 19 Healthcare Services

| # | Service Name | Category | Turnaround / Badge | Key Features |
|---|--------------|----------|-------------------|--------------|
| 1 | **Online Doctor Consultation** | Doctor Consultation | 15-Min Connect | Video/Audio consultation, 7-day free WhatsApp follow-up, digital Rx |
| 2 | **Doctor Home Visits** | Doctor Consultation | Doorstep Clinical | Bedside physical checkups, senior citizen priority, post-discharge review |
| 3 | **Doorstep E-Pharmacy** | Pharmacy & Medicines | 2-Hour Express | 100% genuine certified medicines, flat 20% chronic refill discounts |
| 4 | **Home Diagnostics & Lab Tests** | Diagnostics & Lab | NABL Accredited | Certified phlebotomists, painless vacutainer draw, 6-hr smart PDF reports |
| 5 | **X-Ray & Portable Diagnostics** | Diagnostics & Lab | Bedside Digital | Low-radiation digital X-Ray & 12-lead ECG in bedroom, instant radiologist review |
| 6 | **Specialized Nursing Care** | Home Care & Nursing | GNM/B.Sc Certified | 12h/24h residential shifts, IV infusions, wound dressing, tracheostomy |
| 7 | **Bedside Assistant & Attendant** | Home Care & Nursing | 12h/24h Shifts | Mobility, personal hygiene, feeding, post-operative & paralysis recovery |
| 8 | **Eldercare & Senior Assistance** | Home Care & Nursing | Dedicated Companion | Scheduled vitals logging, medication adherence, companionship walks, SOS alerts |
| 9 | **Physiotherapy at Home** | Rehabilitation | Certified Physios | Stroke recovery, orthopedic rehab, portable electrotherapy (TENS, Ultrasound) |
| 10 | **Dental Care & Oral Health** | Doctor Consultation | Portable Clinic | Ultrasonic scaling, cavity fillings, denture adjustment, senior citizen care |
| 11 | **24/7 Smart Ambulance & SOS** | Emergency & Critical | 8-Min Arrival | Real-time GPS dispatch, onboard ALS/BLS ventilator, oxygen, ER pre-sync |
| 12 | **Blood Bank & Support** | Emergency & Critical | 24/7 Live Network | Real-time blood group stock lookup, voluntary donor coordination, component transit |
| 13 | **Diagnostics & Advanced Imaging** | Diagnostics & Lab | MRI / CT / PET Scans | Zero waiting queue priority slot booking at accredited scan centers, DICOM cloud |
| 14 | **Home Vaccination Service** | Preventive & Care | Cold-Chain Safe | Strict cold-chain maintenance, childhood schedule & adult vaccines (Flu, Hep-B) |
| 15 | **Full Body Preventive Screening** | Preventive & Care | 85+ Parameters | Comprehensive vital package (Cardiac, Liver, Kidney, Thyroid, HbA1c, Vit D/B12) |
| 16 | **Chronic Disease Care Programmes** | Preventive & Care | 360° Management | Tailored disease management for Diabetes, Hypertension, Cardiac & Asthma |
| 17 | **Mental Health & Counseling** | Rehabilitation | 100% Confidential | Confidential 1-on-1 video therapy with licensed clinical psychologists (CBT) |
| 18 | **Premium OPD Memberships** | Preventive & Care | VIP Priority | On-ground Care Buddy for hospital admissions, zero queue wait, up to 30% discounts |
| 19 | **Health Support Rider** | Emergency & Critical | Pick • Support • Drop | Safe hospital transit, full-day patient companion for OPD tests, live GPS tracking |

---

## 🛵 Health Support Rider & Rapido-Style Booking

The dedicated booking page (`/rider/book`) features a **Rapido-style booking experience**:
- **Compact Left Control Panel**: Streamlined width (380px) ensuring the interactive map remains the visual centerpiece.
- **Live Debounced Geocoding (650ms)**: Typing into Pickup or Hospital Drop fields dynamically geocodes coordinates via OpenStreetMap Nominatim, displays a `"Locating on map..."` indicator, updates map pins, and redraws the OSRM route polyline in real-time.
- **Manual Town / Village Address Entry**: Support for detailed rural and semi-urban addresses across Bharat.
- **Pay-First Security Flow**:
  1. Patient selects pickup & hospital destination.
  2. Estimated fare and distance calculated via live route geometry.
  3. Online payment modal pops up (UPI QR, Cards, NetBanking).
  4. Upon payment success, trip is created and an **Automated Tax Invoice** (`NH-INV-YYYYMMDD-XXXX`) is issued.
  5. Live tracking begins with a 4-digit start OTP for rider verification.
- **Policy Enforcement**:
  - *"Once booked, the service cannot be cancelled or refunded."*
  - *"The payment is valid only on that day."*

---

## 🔒 Authentication, Security & KYC

- **Password Security**: Uses Werkzeug's secure hashing (`generate_password_hash` with `scrypt` / `pbkdf2:sha256`). Plaintext passwords from legacy records are automatically upgraded on successful login.
- **Rate-Limiting Protection**: IP + Identifier brute-force defense locks accounts for 30 seconds after 5 failed attempts.
- **Session Protection**: Flask session cookies configured with `HttpOnly=True` and `SameSite='Lax'`.
- **Rider Verification & KYC**:
  - **Two Mandatory Contact Numbers**: Primary phone + Secondary alternate emergency contact (validated for 10 digits each and must be distinct).
  - **Location Type**: City, Town, or Village selection covering all Indian States and Union Territories (36 states/UTs).
  - **Mandatory Individual Photo**: Driver verification document.
  - **Optional Family Photo & Police NOC**: Background check clearance upload.
  - **Zero Cash Policy**: All rider bookings operate strictly on online pre-payment.

---

## 🔑 Official Demo Credentials

Use these verified credentials to test each portal:

| Role | Portal URL | Identifier (Email / Phone) | Password | Demo Persona |
|------|------------|----------------------------|----------|--------------|
| **Patient** | `/login` ➔ `/patient/dashboard` | `patient@nhealth.in` or `9123456780` | `password123` | Suresh Kumar (Visakhapatnam) |
| **Doctor** | `/login` ➔ `/doctor/dashboard` | `doctor@nhealth.in` or `9876543210` | `password123` | Dr. Arjun Reddy, MD |
| **Doctor (Alt)** | `/login` ➔ `/doctor/dashboard` | `priya.sharma@nhealth.in` or `9848011223` | `password123` | Dr. Priya Sharma, MD |
| **Pharmacy** | `/login/pharmacy` ➔ `/pharmacy/dashboard` | `pharmacy@nhealth.in` or `9876543290` | `password123` | Sai Medicals & Pharmacy |
| **Pharmacy (Alt)** | `/login/pharmacy` ➔ `/pharmacy/dashboard` | `pharma@gmail.com` or `9988776655` | `password123` | MedPlus Pharmacy |
| **Lab** | `/login/lab` ➔ `/lab/dashboard` | `lab@nhealth.in` or `9876543299` | `password123` | Apollo Diagnostics Lab |
| **Rider** | `/login/rider` ➔ `/rider/dashboard` | `rider@nhealth.in` or `9876543222` | `password123` | Ravi Varma (Hero Splendor) |

---

## 💾 Database Layer & Resilience

Nhealth uses a hybrid storage engine:
1. **Primary**: **Neon Serverless PostgreSQL** via `ThreadedConnectionPool`.
   - Automatic table schema creation (`users`, `bookings`, `contacts`, `rider_trips`).
   - Resilient connection pooling: Liveness checks automatically detect dropped connections and request fresh ones.
   - Safe rollback wrapper prevents crashes if Neon terminates idle connections.
2. **Secondary Fallback**: **Local JSON Storage** (`data/*.json`).
   - If PostgreSQL is unreachable or unconfigured, the application falls back to `data/users.json`, `data/trips.json`, `data/bookings.json`, and `data/contacts.json`.
   - Data persists across server restarts in both storage modes.

---

## 📡 Complete API Reference

### Public & Informational APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Renders the primary homepage |
| `GET` | `/contact` | Renders the Contact Us page |
| `GET` | `/api/services` | Returns list of all 19 healthcare services (JSON) |
| `GET` | `/api/locations` | Returns list of 15 Andhra Pradesh coverage cities |
| `GET` | `/api/stats` | Returns platform trust metrics and family counts |
| `POST` | `/api/book` | Submits an appointment booking request |
| `POST` | `/api/contact` | Submits a general inquiry message |

### Authentication APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/signup` | Registers new Patient, Doctor, Pharmacy, Lab, or Rider |
| `POST` | `/api/auth/login` | Authenticates user with rate-limiting & session generation |
| `POST, GET` | `/api/auth/logout` | Clears active session and returns JSON response |
| `GET` | `/logout` | Clears session and redirects to role-appropriate login page |

### Patient & Profile APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/patient/dashboard` | Renders Patient Consultation & Health Dashboard |
| `GET` | `/rider/book` | Renders Rapido-Style Rider Booking Page |
| `GET` | `/api/user/profile` | Fetches currently authenticated patient profile |
| `POST` | `/api/user/profile` | Updates patient profile (name, phone, dob, address, etc.) |

### Health Support Rider APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/trip/create` | Creates trip, validates online payment, issues tax invoice |
| `GET` | `/api/trip/<trip_id>/live` | Fetches real-time GPS coordinates, ETA, and trip status |
| `GET` | `/api/trip/<trip_id>/invoice` | Retrieves full printable tax invoice and payment breakdown |
| `POST` | `/api/rider/status` | Toggles rider online/offline duty status |
| `POST` | `/api/rider/location` | Streams live GPS coordinates from rider phone |
| `GET` | `/api/rider/tasks` | Fetches active trip and available dispatch queue |
| `POST` | `/api/rider/accept_task` | Rider claims an open ride request |
| `POST` | `/api/rider/update_task_status` | Updates trip state (`arrived`, `in_progress`, `completed`, `ended`) |
| `POST` | `/api/rider/verify_otp` | Validates 4-digit start OTP provided by patient |
| `GET` | `/api/rider/history` | Returns completed/ended trip history for rider cockpit |

---

## 🚀 Local Development Setup

### 1. Prerequisites
- Python 3.11 or higher
- Git
- Virtual environment tool (`venv`)

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/nhealth2026/Nhealth.git
cd Nhealth

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=nhealth-super-secret-key-2026-secure-session
DATABASE_URL=postgresql://your_user:your_password@your_neon_host/nhealth?sslmode=require
PORT=5000
```
*(Note: If `DATABASE_URL` is omitted, Nhealth automatically runs in local JSON fallback mode without errors.)*

### 4. Run Development Server
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🧪 Running Tests

The project includes unit, integration, and security tests under `tests/`:

```bash
# Run all tests
pytest tests/

# Run tests with verbose output
pytest tests/ -v

# Run specific test suite
pytest tests/test_audit_fixes.py
pytest tests/test_payment_invoice_flow.py
pytest tests/test_rider_flow.py
```

---

## ☁️ Production Deployment

### 1. Render / Railway / Heroku Deployment
The project includes a ready-to-use [`Procfile`](file:///d:/nhealth%20final/Procfile):
```procfile
web: gunicorn app:app
```

**Build & Run Configuration:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Environment Variables**: Set `DATABASE_URL` and `SECRET_KEY` in your cloud dashboard.

### 2. Linux VPS (Ubuntu / Debian + Nginx + Gunicorn)
```bash
# Run via Gunicorn with 4 worker processes
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

---

## 📄 License

This project is licensed under the **MIT License**.  
Copyright (c) 2026 **NHealth Technologies Inc.** All Rights Reserved.

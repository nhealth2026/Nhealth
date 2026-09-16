# Nhealth - Healthcare at Home

Powering the Future of Healthcare at Home - Fast, verified, and complete home medical ecosystem.

## Overview
Nhealth is an enterprise-grade digital healthcare platform and home medical marketplace that connects patients, board-certified doctors, certified diagnostic labs, temperature-controlled pharmacies, and emergency life-support ambulance networks under a single unified ecosystem.

## Key Features
- **Desktop Laptop View (100vh Non-Scrolling Lock)**: Single-screen layout with interactive Andhra Pradesh map, calligraphy, service carousel, and live trust metrics.
- **Dedicated Mobile App Layout (1:1 Native Experience)**: High-resolution artwork backdrop, AI symptom search pill, 4-column service grid (11 services + Doctor promo card), quick actions, floating bottom navigation, and official floating WhatsApp support widget.
- **Next-Gen Telemedicine Virtual Clinic**: Real-time encrypted consultation room featuring live vitals telemetry (Pulse, SpO2, Blood Pressure), synchronized consultation chat, and digital e-prescription generation dispatched directly to WhatsApp.
- **Data-Driven Healthcare Analytics**: Real-time operational intelligence including GMV growth (+24.6% YoY), weekly consultation peak loads, clinical specialty distributions, and 28-minute pharmacy express delivery timelines.
- **Frictionless WhatsApp & Omnichannel Alerts**: Automated booking confirmations, doctor reminders, live GPS tracking for ambulances/medicines, and direct download links for NABL lab reports.

## Comprehensive Healthcare Suite
1. **Doctor Video Consultation**: Starts at Rs 499 (15-min instant telemedicine, 7-day free follow-up, digital Rx)
2. **Doorstep E-Pharmacy**: Express Free > Rs 500 (100% genuine certified medicines, 2-hour delivery guarantee)
3. **Home Diagnostics & Lab Tests**: Packages from Rs 699 (NABL/CAP accredited, painless blood draw, 6-hour verified smart PDF reports)
4. **Specialized Nursing Care**: Per Shift from Rs 1,200 (Registered nurses, 12h/24h shifts, vital monitoring, post-op care)
5. **24/7 Smart Ambulance SOS**: Emergency Toll-Free (8-minute average arrival time, onboard ALS/BLS ventilator & O2, hospital ER pre-sync)
6. **Full Body Preventive Health Checkup**: Comprehensive Rs 1,999 (85+ parameters covering Cardiac, Liver, Kidney, Diabetes with free MD consultation)

## Technology Stack
- **Backend**: Python 3.11+, Flask Web Framework, Gunicorn WSGI Server
- **Frontend**: Semantic HTML5, Modern CSS3 (Variables, Flexbox, CSS Grid), Vanilla JavaScript (ES6+ Async/Await)
- **Styling & Icons**: Font Awesome 6.4.2, Google Fonts (Plus Jakarta Sans, Outfit, Caveat)
- **Deployment**: Render, Gunicorn, dynamic PORT binding

## Deployment on Render
This project is configured for 1-click deployment on [Render](https://render.com).

### Render Web Service Configuration:
- **Build Command**: pip install -r requirements.txt
- **Start Command**: gunicorn app:app
- **Environment**: Python 3
- **Port**: Bound automatically via PORT environment variable

## Local Setup
```bash
git clone https://github.com/nhealth2026/Nhealth.git
cd Nhealth
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 in your browser.

## License
MIT License. Copyright (c) 2026 NHealth Technologies Inc.

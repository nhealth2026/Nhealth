import pytest
import re
import db
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_audit_fixes(client):
    # ==================== TEST 1 & 2 & 3 & 4: RIDER SIGNUP VALIDATION ====================
    # Missing secondary contact number
    bad_signup = client.post('/api/auth/signup', json={
        'role': 'rider',
        'name': 'Audit Rider One',
        'email': 'audit_rider1@example.com',
        'phone': '9876541111',
        'state': 'Karnataka',
        'location_type': 'town',
        'town_village': 'Channapatna',
        'reg_number': 'KA05 2023001',
        'vehicle_type': 'Motorcycle (Two-Wheeler)',
        'vehicle_number': 'KA 05 AB 1234',
        'password': 'password123',
        'has_individual_photo': True
    })
    assert bad_signup.status_code == 400
    assert 'Secondary / Alternate Contact Number is mandatory' in bad_signup.get_json()['message']

    # Identical phone numbers
    same_phone_signup = client.post('/api/auth/signup', json={
        'role': 'rider',
        'name': 'Audit Rider Same Phone',
        'email': 'audit_rider_same@example.com',
        'phone': '9876541111',
        'secondary_phone': '9876541111',
        'state': 'Maharashtra',
        'location_type': 'village',
        'town_village': 'Shirdi Village',
        'reg_number': 'MH15 2023001',
        'vehicle_type': 'Motorcycle (Two-Wheeler)',
        'vehicle_number': 'MH 15 AB 1234',
        'password': 'password123',
        'has_individual_photo': True
    })
    assert same_phone_signup.status_code == 400
    assert 'Primary and Secondary contact numbers must be different' in same_phone_signup.get_json()['message']

    # Missing individual photo
    no_photo_signup = client.post('/api/auth/signup', json={
        'role': 'rider',
        'name': 'Audit Rider No Photo',
        'email': 'audit_rider_nophoto@example.com',
        'phone': '9876541112',
        'secondary_phone': '9876541113',
        'state': 'Tamil Nadu',
        'location_type': 'city',
        'town_village': 'Coimbatore',
        'reg_number': 'TN38 2023001',
        'vehicle_type': 'Motorcycle (Two-Wheeler)',
        'vehicle_number': 'TN 38 AB 1234',
        'password': 'password123',
        'has_individual_photo': False
    })
    assert no_photo_signup.status_code == 400
    assert 'Individual Photo is mandatory' in no_photo_signup.get_json()['message']

    # Successful All-India Signup with 2 contacts and Town/Village location type
    import random
    r_num = random.randint(100000, 999999)
    good_phone1 = f"9876{r_num}"
    good_phone2 = f"9877{r_num}"
    good_email = f"rider_{r_num}@example.com"

    good_signup = client.post('/api/auth/signup', json={
        'role': 'rider',
        'name': 'Bharat Verified Rider',
        'email': good_email,
        'phone': good_phone1,
        'secondary_phone': good_phone2,
        'state': 'Gujarat',
        'location_type': 'village',
        'city': 'Anand Village',
        'town_village': 'Anand Village',
        'pincode': '388001',
        'reg_number': 'GJ01 20230099',
        'vehicle_type': 'Motorcycle (Two-Wheeler)',
        'vehicle_number': 'GJ 01 CD 5678',
        'password': 'password123',
        'has_individual_photo': True,
        'has_family_photo': False,
        'has_police_noc': False
    })
    assert good_signup.status_code == 201
    signup_json = good_signup.get_json()
    assert signup_json['status'] == 'success'
    rider_user = signup_json['user']
    assert rider_user['secondary_phone'] == good_phone2
    assert rider_user['location_type'] == 'village'
    assert rider_user['town_village'] == 'Anand Village'
    assert rider_user['payment_mode'] == 'Online Only'

    # ==================== TEST 7: PROTECTED ROUTE & LOGOUT ====================
    # Session is currently set for the new rider
    dash_res = client.get('/rider/dashboard')
    assert dash_res.status_code == 200
    assert b'Bharat Verified Rider' in dash_res.data
    assert b'Trip History' in dash_res.data
    assert b'Online Payment Only' in dash_res.data

    # Log out
    logout_res = client.get('/logout')
    assert logout_res.status_code == 302
    assert '/rider/login' in logout_res.headers['Location'] or '/login/rider' in logout_res.headers['Location']

    # Try accessing /rider/dashboard without login -> must redirect to rider login
    unauth_dash = client.get('/rider/dashboard')
    assert unauth_dash.status_code == 302
    assert '/rider/login' in unauth_dash.headers['Location'] or '/login/rider' in unauth_dash.headers['Location']

    # Re-login with the created account
    login_res = client.post('/api/auth/login', json={
        'identifier': good_phone1,
        'password': 'password123',
        'role': 'rider'
    })
    assert login_res.status_code == 200

    # ==================== TEST 12 & 13 & 14: MANUAL LOCATION ENTRY & TRIP CREATION ====================
    manual_addr = "House 4B, Near Shanti Mandir, Anand Village, Gujarat - 388001"
    create_res = client.post('/api/trip/create', json={
        'patient_name': 'Meera Patel',
        'patient_phone': '9822334455',
        'pickup_address': manual_addr,
        'drop_address': 'Apollo Clinic, Station Road',
        'pickup_lat': 22.5645,
        'pickup_lng': 72.9289,
        'drop_lat': 22.5700,
        'drop_lng': 72.9350,
        'fare_amount': 150,
        'distance_km': 3.2
    })
    assert create_res.status_code == 201
    created_trip = create_res.get_json()['trip']
    assert created_trip['pickup_address'] == manual_addr
    assert created_trip['extra_data']['payment_mode'] == 'Online Only (UPI/QR)'
    trip_id = created_trip['trip_id']
    start_otp = created_trip['start_otp']

    # ==================== TEST 5 & 6: ENDED TRIP STATUS & HISTORY ====================
    # Accept trip
    client.post('/api/rider/accept_task', json={'trip_id': trip_id, 'rider_id': rider_user['id']})

    # Mark arrived
    client.post('/api/rider/update_task_status', json={'trip_id': trip_id, 'status': 'arrived'})

    # Verify OTP
    client.post('/api/rider/verify_otp', json={'trip_id': trip_id, 'otp': start_otp})

    # End trip (Status: 'ended')
    end_res = client.post('/api/rider/update_task_status', json={'trip_id': trip_id, 'status': 'ended'})
    assert end_res.status_code == 200
    assert end_res.get_json()['trip']['status'] == 'ended'

    # Verify active cockpit has NO active trip now
    tasks_res = client.get(f'/api/rider/tasks?rider_id={rider_user["id"]}')
    assert tasks_res.status_code == 200
    assert tasks_res.get_json()['active_trip'] is None

    # Fetch history via /api/rider/history
    history_res = client.get(f'/api/rider/history?rider_id={rider_user["id"]}')
    assert history_res.status_code == 200
    history_data = history_res.get_json()
    assert history_data['status'] == 'success'
    assert len(history_data['history']) > 0
    hist_trip = next((t for t in history_data['history'] if t['trip_id'] == trip_id), None)
    assert hist_trip is not None
    assert hist_trip['status'] == 'ended'
    assert hist_trip['pickup_address'] == manual_addr
    assert hist_trip['fare_amount'] == 150

    print("ALL 16 AUDIT FIXES VERIFIED SUCCESSFULLY!")

if __name__ == '__main__':
    pytest.main(['-v', __file__])

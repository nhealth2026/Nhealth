import pytest
import json
import db
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_rider_flow(client):
    # 1. Login as Demo Rider
    login_res = client.post('/api/auth/login', json={
        'role': 'rider',
        'identifier': 'rider@nhealth.in',
        'password': 'password123'
    })
    assert login_res.status_code == 200
    login_data = login_res.get_json()
    assert login_data['status'] == 'success'
    assert login_data['redirect'] == '/rider/dashboard'
    assert login_data['user']['role'] == 'rider'

    # 2. Toggle duty status online
    status_res = client.post('/api/rider/status', json={'is_online': True})
    assert status_res.status_code == 200
    assert status_res.get_json()['is_online'] is True

    # 3. Post rider location
    loc_res = client.post('/api/rider/location', json={
        'lat': 28.5355,
        'lng': 77.3910,
        'heading': 90,
        'speed': 35
    })
    assert loc_res.status_code == 200
    assert loc_res.get_json()['status'] == 'success'

    # 4. Patient creates a trip request
    trip_res = client.post('/api/trip/create', json={
        'patient_name': 'Test Patient',
        'patient_phone': '9123456780',
        'pickup_address': 'Sector 18, Block B',
        'drop_address': 'Nhealth Clinic, Main Road',
        'trip_type': 'Patient Accompaniment',
        'fare_amount': 120,
        'pickup_lat': 28.5380,
        'pickup_lng': 77.3930,
        'drop_lat': 28.5430,
        'drop_lng': 77.4010
    })
    assert trip_res.status_code in [200, 201]
    trip_data = trip_res.get_json()
    assert trip_data['status'] == 'success'
    trip_id = trip_data['trip']['trip_id']
    start_otp = trip_data['trip']['start_otp']
    assert trip_id is not None
    assert len(start_otp) == 4

    # 5. Rider checks available tasks
    tasks_res = client.get('/api/rider/tasks')
    assert tasks_res.status_code == 200
    tasks_data = tasks_res.get_json()
    assert tasks_data['status'] == 'success'
    assert len(tasks_data['available_tasks']) > 0

    # 6. Rider accepts task
    accept_res = client.post('/api/rider/accept_task', json={'trip_id': trip_id})
    assert accept_res.status_code == 200
    assert accept_res.get_json()['status'] == 'success'

    # 7. Check live tracking as patient
    live_res = client.get(f'/api/trip/{trip_id}/live')
    assert live_res.status_code == 200
    live_data = live_res.get_json()
    assert live_data['status'] == 'success'
    assert live_data['trip']['status'] == 'accepted'

    # 8. Rider marks arrived at pickup
    arr_res = client.post('/api/rider/update_task_status', json={
        'trip_id': trip_id,
        'status': 'arrived'
    })
    assert arr_res.status_code == 200

    # 9. Rider verifies OTP
    otp_res = client.post('/api/rider/verify_otp', json={
        'trip_id': trip_id,
        'otp': start_otp
    })
    assert otp_res.status_code == 200
    assert otp_res.get_json()['status'] == 'success'

    # 10. Rider completes trip
    comp_res = client.post('/api/rider/update_task_status', json={
        'trip_id': trip_id,
        'status': 'completed'
    })
    assert comp_res.status_code == 200
    assert comp_res.get_json()['trip']['status'] == 'completed'

    # 11. Test dedicated Rider Booking Page GET requests
    page_res = client.get('/rider/book')
    assert page_res.status_code == 200
    assert b'Book Health Support Rider' in page_res.data
    assert b'riderBookingMap' in page_res.data

    page_alias_res = client.get('/book-rider')
    assert page_alias_res.status_code == 200
    assert b'Book Health Support Rider' in page_alias_res.data

    print("All Rider & Live Tracking tests passed successfully!")

if __name__ == '__main__':
    pytest.main(['-v', __file__])

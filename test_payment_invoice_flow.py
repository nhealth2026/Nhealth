"""
Tests for:
1. Patient paying first before booking/dispatching rider.
2. Required cancellation policy message: "Once booked, the service cannot be cancelled or refunded."
3. Required validity policy message: "The payment is valid only on that day."
4. Automatic invoice numbering generation (e.g. NH-INV-YYYYMMDD-XXXX).
5. Tax invoice retrieval endpoint.
"""
import pytest
from app import app
import db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_automatic_invoice_and_payment_flow(client):
    # 1. Automatic invoice numbering verification
    inv_num1 = db.generate_next_invoice_number("NH-INV")
    assert inv_num1.startswith("NH-INV-")
    
    # 2. Create trip through API with online payment
    res = client.post('/api/trip/create', json={
        'patient_name': 'Anita Sharma',
        'patient_phone': '9876500112',
        'pickup_address': 'Plot 45, Revenue Colony, Vijayawada',
        'drop_address': 'Andhra Hospital, Governorpet',
        'fare_amount': 160,
        'distance_km': 4.2,
        'payment_id': 'PAY-UPI-TEST-2026',
        'payment_mode': 'Online UPI'
    })
    
    assert res.status_code == 201
    data = res.get_json()
    assert data['status'] == 'success'
    
    trip = data['trip']
    invoice = data['invoice']
    
    # Verify automatic invoice numbering in trip and invoice
    assert invoice['invoice_number'].startswith("NH-INV-")
    assert trip['invoice_number'] == invoice['invoice_number']
    
    # Verify policy messages
    expected_cancel = "Once booked, the service cannot be cancelled or refunded."
    expected_valid = "The payment is valid only on that day."
    assert invoice['cancellation_policy'] == expected_cancel
    assert invoice['validity_policy'] == expected_valid
    assert trip['extra_data']['cancellation_policy'] == expected_cancel
    assert trip['extra_data']['validity_policy'] == expected_valid
    
    # Verify payment status
    assert invoice['payment_status'] == 'PAID'
    assert 'PAID' in trip['extra_data']['payment_status']
    
    # 3. Test invoice retrieval API
    trip_id = trip['trip_id']
    inv_res = client.get(f'/api/trip/{trip_id}/invoice')
    assert inv_res.status_code == 200
    inv_data = inv_res.get_json()
    assert inv_data['status'] == 'success'
    fetched_inv = inv_data['invoice']
    assert fetched_inv['invoice_number'] == invoice['invoice_number']
    assert fetched_inv['cancellation_policy'] == expected_cancel
    assert fetched_inv['validity_policy'] == expected_valid

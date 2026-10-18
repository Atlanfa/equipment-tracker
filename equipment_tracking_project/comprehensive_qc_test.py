#!/usr/bin/env python3
"""
Comprehensive test script for the QC Sign-off feature
This script demonstrates all aspects of the Quality Control Sign-off functionality
"""

import requests
import json
from datetime import date, datetime
import time

BASE_URL = "http://127.0.0.1:8000"

def test_equipment_lookup():
    """Test equipment lookup functionality with real data"""
    print("\n=== Testing Equipment Lookup ===")
    
    # Test with real barcode
    response = requests.get(f"{BASE_URL}/api/lookup-equipment/", params={'barcode': 'ASL0000029278'})
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ Equipment found: {data['equipment_name']}")
            print(f"   Order: {data['order_number']}")
            print(f"   Quantity: {data['total_quantity']}")
            print(f"   Date: {data['date']}")
            print(f"   Source: {data['source']}")
            return data
        else:
            print(f"❌ Lookup failed: {data['error']}")
    else:
        print(f"❌ Request failed with status {response.status_code}")
    
    return None

def test_qc_signoff_submission(equipment_data=None):
    """Test QC sign-off submission"""
    print("\n=== Testing QC Sign-off Submission ===")
    
    if equipment_data:
        barcode = 'ASL0000029278'
        order_number = equipment_data['order_number']
        equipment_name = equipment_data['equipment_name']
        quantity = equipment_data['total_quantity']
    else:
        barcode = 'TEST_BARCODE_001'
        order_number = 'TEST_ORDER_001'
        equipment_name = 'Test Equipment'
        quantity = 5
    
    qc_data = {
        'equipment_barcode': barcode,
        'order_number': order_number,
        'inspector_name': 'Jane Doe',
        'inspection_date': date.today().strftime('%Y-%m-%d'),
        'qc_status': 'passed',
        'quantity': quantity,
        'inspection_notes': 'All units passed comprehensive quality inspection.',
        'corrective_actions': '',
        'printer_name': 'HP_QC_Printer_01',
        'print_sticker': True,
        'order_completion': 'all',
        'completed_items': []
    }
    
    response = requests.post(
        f"{BASE_URL}/api/qc-signoff/",
        headers={'Content-Type': 'application/json'},
        data=json.dumps(qc_data)
    )
    
    if response.status_code == 201:
        data = response.json()
        if data['success']:
            signoff = data['signoff']
            print(f"✅ QC Sign-off submitted successfully")
            print(f"   ID: {signoff['id']}")
            print(f"   Equipment: {signoff['equipment_name']}")
            print(f"   Order: {signoff['order_number']}")
            print(f"   Inspector: {signoff['inspector_name']}")
            print(f"   Status: {signoff['qc_status']}")
            print(f"   Quantity: {signoff['quantity']}")
            return signoff
        else:
            print(f"❌ Sign-off submission failed: {data['error']}")
    else:
        print(f"❌ Request failed with status {response.status_code}")
        if response.content:
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
    
    return None

def test_partial_completion():
    """Test partial completion functionality"""
    print("\n=== Testing Partial Completion ===")
    
    qc_data = {
        'equipment_barcode': 'PARTIAL_TEST_001',
        'order_number': 'ORDER_PARTIAL_001',
        'inspector_name': 'Mike Johnson',
        'inspection_date': date.today().strftime('%Y-%m-%d'),
        'qc_status': 'partial',
        'quantity': 10,
        'inspection_notes': 'Partial inspection completed. 7 units passed, 3 require rework.',
        'corrective_actions': 'Units BC001, BC002, BC003 need cable replacement before re-inspection.',
        'printer_name': 'HP_QC_Printer_01',
        'print_sticker': True,
        'order_completion': 'partial',
        'completed_items': ['BC004', 'BC005', 'BC006', 'BC007', 'BC008', 'BC009', 'BC010']
    }
    
    response = requests.post(
        f"{BASE_URL}/api/qc-signoff/",
        headers={'Content-Type': 'application/json'},
        data=json.dumps(qc_data)
    )
    
    if response.status_code == 201:
        data = response.json()
        if data['success']:
            signoff = data['signoff']
            print(f"✅ Partial QC Sign-off submitted successfully")
            print(f"   ID: {signoff['id']}")
            print(f"   Status: {signoff['qc_status']}")
            print(f"   Completion: {signoff['order_completion']}")
            print(f"   Completed Items: {len(signoff['completed_items'])} out of {signoff['quantity']}")
            print(f"   Corrective Actions: {signoff['corrective_actions'][:50]}...")
            return signoff
        else:
            print(f"❌ Partial sign-off failed: {data['error']}")
    else:
        print(f"❌ Request failed with status {response.status_code}")
    
    return None

def test_qc_history():
    """Test QC sign-off history retrieval"""
    print("\n=== Testing QC Sign-off History ===")
    
    response = requests.get(f"{BASE_URL}/api/qc-signoffs/")
    
    if response.status_code == 200:
        data = response.json()
        signoffs = data.get('signoffs', [])
        print(f"✅ Retrieved {len(signoffs)} QC sign-off records")
        
        if signoffs:
            print("\nRecent Sign-offs:")
            for i, signoff in enumerate(signoffs[:3]):  # Show first 3
                print(f"   {i+1}. {signoff['equipment_name']} - Order #{signoff['order_number']}")
                print(f"      Status: {signoff['qc_status']} | Inspector: {signoff['inspector_name']}")
                print(f"      Date: {signoff['inspection_date']} | Quantity: {signoff['quantity']}")
        
        return signoffs
    else:
        print(f"❌ Request failed with status {response.status_code}")
    
    return []

def test_search_functionality():
    """Test equipment search functionality"""
    print("\n=== Testing Equipment Search ===")
    
    search_terms = ['A&H', 'Digital', 'Mixer']
    
    for term in search_terms:
        search_data = {'search_term': term}  # Fixed parameter name
        response = requests.post(
            f"{BASE_URL}/api/search-equipment/",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(search_data)
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                results = data.get('results', [])
                print(f"✅ Search for '{term}': {len(results)} results found")
                if results:
                    print(f"   First result: {results[0]['name']}")
            else:
                print(f"❌ Search for '{term}' failed: {data['error']}")
        else:
            print(f"❌ Search request failed with status {response.status_code}")

def main():
    """Run comprehensive tests"""
    print("=== QC Sign-off System Comprehensive Test ===")
    print(f"Testing against: {BASE_URL}")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Equipment Lookup
    equipment_data = test_equipment_lookup()
    
    # Test 2: QC Sign-off Submission (with real data if available)
    signoff_data = test_qc_signoff_submission(equipment_data)
    
    # Test 3: Partial Completion
    partial_data = test_partial_completion()
    
    # Test 4: History Retrieval
    history_data = test_qc_history()
    
    # Test 5: Search Functionality
    test_search_functionality()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"✅ Equipment Lookup: {'PASSED' if equipment_data else 'FAILED'}")
    print(f"✅ QC Sign-off: {'PASSED' if signoff_data else 'FAILED'}")
    print(f"✅ Partial Completion: {'PASSED' if partial_data else 'FAILED'}")
    print(f"✅ History Retrieval: {'PASSED' if history_data else 'FAILED'}")
    print(f"\nTotal QC Records in System: {len(history_data)}")
    
    print("\n=== Integration Test Complete ===")
    print("\nNext Steps:")
    print("1. Open http://127.0.0.1:8000/ to test the frontend")
    print("2. Navigate to the 'Quality Control Sign-off' tab")
    print("3. Test barcode input with: ASL0000029278")
    print("4. Verify auto-population of equipment and order information")
    print("5. Submit a test QC sign-off and verify it appears in history")

if __name__ == "__main__":
    main()

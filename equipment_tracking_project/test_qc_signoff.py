#!/usr/bin/env python
"""
Test script for QC Sign-off functionality
Run this script to test the API endpoints for Quality Control Sign-off
"""

import requests
import json
import datetime

# API base URL
BASE_URL = "http://127.0.0.1:8000"

def test_qc_signoff_submission():
    """Test submitting a QC sign-off"""
    print("Testing QC Sign-off submission...")
    
    # Sample QC sign-off data
    qc_data = {
        "equipment_barcode": "TEST001",
        "order_number": "ORD-12345",
        "inspector_name": "John Doe",
        "inspection_date": datetime.date.today().strftime("%Y-%m-%d"),
        "qc_status": "passed",
        "quantity": 25,
        "inspection_notes": "All units passed visual inspection and functionality tests.",
        "corrective_actions": "",
        "printer_name": "John Doe",
        "print_sticker": True,
        "order_completion": "all",
        "completed_items": [],
        "use_default_notes": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/qc-signoff/",
            data=json.dumps(qc_data),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Data: {response.json()}")
        
        if response.status_code == 201:
            print("✅ QC Sign-off submitted successfully!")
            return response.json()['signoff']['id']
        else:
            print("❌ QC Sign-off submission failed!")
            return None
            
    except Exception as e:
        print(f"❌ Error during QC sign-off submission: {str(e)}")
        return None

def test_equipment_lookup():
    """Test equipment lookup by barcode"""
    print("\nTesting equipment lookup...")
    
    lookup_data = {
        "barcode": "TEST001"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/lookup-equipment/",
            data=json.dumps(lookup_data),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Data: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Equipment lookup successful!")
        else:
            print("❌ Equipment lookup failed (this is expected if no matching equipment exists)")
            
    except Exception as e:
        print(f"❌ Error during equipment lookup: {str(e)}")

def test_qc_signoffs_list():
    """Test retrieving QC sign-offs list"""
    print("\nTesting QC sign-offs list...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/qc-signoffs/")
        
        print(f"Response Status: {response.status_code}")
        result = response.json()
        print(f"Found {result.get('count', 0)} QC sign-offs")
        
        if response.status_code == 200:
            print("✅ QC sign-offs list retrieved successfully!")
        else:
            print("❌ QC sign-offs list retrieval failed!")
            
    except Exception as e:
        print(f"❌ Error retrieving QC sign-offs: {str(e)}")

def test_partial_completion_signoff():
    """Test QC sign-off with partial item completion"""
    print("\nTesting QC Sign-off with partial completion...")
    
    qc_data = {
        "equipment_barcode": "PARTIAL001",
        "order_number": "ORD-67890",
        "inspector_name": "Jane Smith",
        "inspection_date": datetime.date.today().strftime("%Y-%m-%d"),
        "qc_status": "partial",
        "quantity": 10,
        "inspection_notes": "Some items need additional inspection.",
        "corrective_actions": "Schedule re-inspection for failed items.",
        "printer_name": "Jane Smith",
        "print_sticker": True,
        "order_completion": "partial",
        "completed_items": ["ITEM001", "ITEM002", "ITEM003"],
        "use_default_notes": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/qc-signoff/",
            data=json.dumps(qc_data),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Data: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Partial completion QC Sign-off submitted successfully!")
        else:
            print("❌ Partial completion QC Sign-off submission failed!")
            
    except Exception as e:
        print(f"❌ Error during partial completion sign-off: {str(e)}")

if __name__ == "__main__":
    print("=== QC Sign-off API Testing ===\n")
    
    # Test basic QC sign-off submission
    signoff_id = test_qc_signoff_submission()
    
    # Test equipment lookup
    test_equipment_lookup()
    
    # Test QC sign-offs list
    test_qc_signoffs_list()
    
    # Test partial completion
    test_partial_completion_signoff()
    
    print("\n=== Testing Complete ===")
    print("\nNote: If you see 'Equipment not found' messages, that's expected")
    print("since we haven't added test equipment data to the database yet.")
    print("\nYou can now:")
    print("1. Access the Django admin at http://127.0.0.1:8000/admin/")
    print("2. View the main application at http://127.0.0.1:8000/")
    print("3. Test the QC Sign-off form in the 'Quality Control Sign-off' tab")

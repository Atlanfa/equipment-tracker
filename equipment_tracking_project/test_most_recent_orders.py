#!/usr/bin/env python3
"""
Test script to verify most recent order lookup functionality
"""

import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking_project.settings')
django.setup()

from equipment_tracking_app.models import Barcode, OrderEquipment

def test_most_recent_orders():
    """Test that API returns most recent order data"""
    print('=== Testing Multiple Barcodes for Most Recent Orders ===')

    # Get some sample barcodes
    barcodes = Barcode.objects.all()[:5]
    
    for barcode_obj in barcodes:
        print(f'\nTesting Barcode: {barcode_obj.barcode}')
        
        # Check how many orders this equipment has
        orders = OrderEquipment.objects.filter(equipment=barcode_obj).order_by('-order__return_date')
        print(f'  Equipment: {barcode_obj.equipment.name}')
        print(f'  Total Orders: {orders.count()}')
        
        if orders.exists():
            most_recent = orders.first()
            print(f'  Most Recent Order: {most_recent.order.name} (Date: {most_recent.order.return_date})')
        
        # Test API
        try:
            response = requests.get('http://127.0.0.1:8000/api/lookup-equipment/', 
                                  params={'barcode': barcode_obj.barcode})
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f'  API Result: Order {data["order_number"]} on {data["date"]} (Source: {data["source"]})')
                    
                    # Verify this matches the most recent order
                    if orders.exists():
                        expected_order = orders.first().order.name
                        expected_date = orders.first().order.return_date.strftime('%Y-%m-%d')
                        
                        if data["order_number"] == expected_order and data["date"] == expected_date:
                            print(f'  ✅ MATCH: API returned most recent order')
                        else:
                            print(f'  ❌ MISMATCH: Expected {expected_order} on {expected_date}')
                    
                else:
                    print(f'  API Error: {data["error"]}')
            else:
                print(f'  API Failed: {response.status_code}')
                
        except Exception as e:
            print(f'  Test Error: {str(e)}')

if __name__ == "__main__":
    test_most_recent_orders()

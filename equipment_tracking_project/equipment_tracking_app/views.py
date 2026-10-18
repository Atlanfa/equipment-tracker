from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import EquipmentEntry, Note, QCStaff, Equipment, Location, QCSignoff, Barcode, Order, OrderEquipment
from collections import defaultdict
from django.db.models import Sum, Q

def equipment_tracking_view(request):
    equipment_entries = EquipmentEntry.objects.all()
    notes = Note.objects.all()

    # Group equipment entries by order and equipment name
    grouped_entries = defaultdict(lambda: defaultdict(list))
    for entry in equipment_entries:
        grouped_entries[entry.order_name][entry.equipment_name].append(entry)

    # Calculate total quantities for grouped entries
    grouped_totals = {
        order_name: {
            equipment_name: {
                'total_amount': sum(e.amount for e in entries),
                'entries': entries
            }
            for equipment_name, entries in equipment_dict.items()
        }
        for order_name, equipment_dict in grouped_entries.items()
    }

    context = {
        'grouped_totals': grouped_totals,
        'qc_staff': QCStaff.objects.all(),
        'notes': notes,
    }
    return render(request, 'equipment_tracking.html', context)

@csrf_exempt
def update_equipment_entry(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entry_id = data.get('id')
        field = data.get('field')
        value = data.get('value')

        try:
            entry = EquipmentEntry.objects.get(id=entry_id)
            if field in ['qc_passed', 'in_repair']:
                setattr(entry, field, value)  # Update the specified field
                entry.save()
                return JsonResponse({'success': True, 'message': f'{field} updated successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid field.'})
        except EquipmentEntry.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Entry not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def add_note_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note_content = data.get('content')
            highlight_color = data.get('highlight_color')

            if not note_content:
                return JsonResponse({'error': 'Note content is required.'}, status=400)

            # Save the note to the database
            note = Note.objects.create(content=note_content, highlight_color=highlight_color)

            # Return a success response
            return JsonResponse({
                'message': 'Note added successfully.',
                'note_id': note.id,
                'content': note.content,
                'highlight_color': note.highlight_color,
                'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def search_equipment_view(request):
    """
    API endpoint to search for equipment by name or barcode
    Returns equipment details with associated barcodes and locations
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            search_term = data.get('search_term', '').strip()

            if not search_term:
                return JsonResponse({'success': False, 'error': 'Search term is required.'})

            # Search for equipment by name or barcode
            equipment_results = []
            
            # Search by equipment name (case-insensitive)
            equipment_by_name = Equipment.objects.filter(
                name__icontains=search_term
            ).prefetch_related('barcodes', 'locations')
            
            # Search by barcode
            barcodes_found = Barcode.objects.filter(
                barcode__icontains=search_term
            ).select_related('equipment').prefetch_related('equipment__locations')
            
            # Combine results and avoid duplicates
            found_equipment = set()
            
            # Add equipment found by name
            for equipment in equipment_by_name:
                found_equipment.add(equipment)
            
            # Add equipment found by barcode
            for barcode in barcodes_found:
                found_equipment.add(barcode.equipment)
            
            # Format results
            for equipment in found_equipment:
                equipment_data = {
                    'id': equipment.id,
                    'name': equipment.name,
                    'description': equipment.description,
                    'barcodes': [
                        {
                            'id': barcode.id,
                            'barcode': barcode.barcode,
                            'assigned_at': barcode.assigned_at.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        for barcode in equipment.barcodes.all()
                    ],
                    'locations': [
                        {
                            'id': location.id,
                            'aile': location.aile,
                            'shelf': location.shelf,
                            'row': location.row
                        }
                        for location in equipment.locations.all()
                    ]
                }
                equipment_results.append(equipment_data)
            
            return JsonResponse({
                'success': True,
                'results': equipment_results,
                'count': len(equipment_results)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'An error occurred while searching: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def qc_signoff_view(request):
    """
    API endpoint to submit QC sign-off records
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract form data
            equipment_barcode = data.get('equipment_barcode', '').strip()
            order_number = data.get('order_number', '').strip()
            inspector_name = data.get('inspector_name', '').strip()
            inspection_date = data.get('inspection_date')
            qc_status = data.get('qc_status', 'passed')
            quantity = data.get('quantity', 0)
            inspection_notes = data.get('inspection_notes', 'All units passed visual inspection and functionality tests.')
            corrective_actions = data.get('corrective_actions', '')
            printer_name = data.get('printer_name', '')
            print_sticker = data.get('print_sticker', True)
            order_completion = data.get('order_completion', 'all')
            completed_items = data.get('completed_items', [])
            use_default_notes = data.get('use_default_notes', True)
            
            # Validate required fields
            if not all([equipment_barcode, order_number, inspector_name, inspection_date, printer_name]):
                return JsonResponse({
                    'success': False,
                    'error': 'All required fields must be provided.'
                }, status=400)
            
            # Try to find equipment name from existing equipment entries
            equipment_name = ''
            try:
                # Search for equipment in EquipmentEntry table
                equipment_entry = EquipmentEntry.objects.filter(
                    Q(equipment_name__icontains=equipment_barcode) |
                    Q(barcode__icontains=equipment_barcode) |
                    Q(order_name=order_number)
                ).first()
                
                if equipment_entry:
                    equipment_name = equipment_entry.equipment_name
                else:
                    # Fallback: try Equipment table
                    equipment = Equipment.objects.filter(
                        name__icontains=equipment_barcode
                    ).first()
                    if equipment:
                        equipment_name = equipment.name
                    else:
                        equipment_name = f"Equipment ({equipment_barcode})"
                        
            except Exception:
                equipment_name = f"Equipment ({equipment_barcode})"
            
            # Create QC sign-off record
            qc_signoff = QCSignoff.objects.create(
                equipment_barcode=equipment_barcode,
                equipment_name=equipment_name,
                order_number=order_number,
                inspector_name=inspector_name,
                inspection_date=inspection_date,
                qc_status=qc_status,
                quantity=int(quantity),
                inspection_notes=inspection_notes,
                corrective_actions=corrective_actions,
                printer_name=printer_name,
                print_sticker=print_sticker,
                order_completion=order_completion,
                completed_items=completed_items,
                use_default_notes=use_default_notes
            )
            
            # Return success response with sign-off data
            response_data = {
                'success': True,
                'message': 'QC sign-off submitted successfully',
                'signoff': {
                    'id': qc_signoff.id,
                    'equipment_barcode': qc_signoff.equipment_barcode,
                    'equipment_name': qc_signoff.equipment_name,
                    'order_number': qc_signoff.order_number,
                    'inspector_name': qc_signoff.inspector_name,
                    'inspection_date': str(qc_signoff.inspection_date),
                    'qc_status': qc_signoff.qc_status,
                    'quantity': qc_signoff.quantity,
                    'inspection_notes': qc_signoff.inspection_notes,
                    'corrective_actions': qc_signoff.corrective_actions,
                    'printer_name': qc_signoff.printer_name,
                    'print_sticker': qc_signoff.print_sticker,
                    'order_completion': qc_signoff.order_completion,
                    'completed_items': qc_signoff.completed_items,
                    'created_at': qc_signoff.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
            return JsonResponse(response_data, status=201)
            
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': f'Invalid data format: {str(e)}'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'An error occurred while processing the sign-off: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def lookup_equipment_by_barcode(request):
    """
    API endpoint to lookup equipment information by barcode
    Accepts both GET and POST requests
    """
    if request.method in ['POST', 'GET']:
        try:
            # Get barcode from either POST data or GET parameters
            if request.method == 'POST':
                data = json.loads(request.body)
                barcode = data.get('barcode', '').strip()
            else:  # GET
                barcode = request.GET.get('barcode', '').strip()
            
            if not barcode:
                return JsonResponse({'success': False, 'error': 'Barcode is required.'})
            
            # First, try to find in the Barcode model
            try:
                barcode_obj = Barcode.objects.get(barcode=barcode)
                equipment = barcode_obj.equipment
                
                # Look for orders that contain this equipment, ordered by most recent return date
                order_equipments = OrderEquipment.objects.filter(
                    equipment=barcode_obj
                ).select_related('order').order_by('-order__return_date')
                
                if order_equipments.exists():
                    # Use the most recent order
                    most_recent_order_equipment = order_equipments.first()
                    most_recent_order = most_recent_order_equipment.order
                    
                    # Find all equipment entries in this order with the same equipment name
                    # and sum their quantities
                    total_quantity = OrderEquipment.objects.filter(
                        order=most_recent_order,
                        equipment__name=equipment.name
                    ).aggregate(total=Sum('amount'))['total'] or 0
                    
                    return JsonResponse({
                        'success': True,
                        'equipment_name': equipment.name,
                        'order_number': most_recent_order.name,
                        'total_quantity': total_quantity,
                        'date': most_recent_order.return_date.strftime('%Y-%m-%d'),
                        'source': 'barcode_model',
                        'order_date': most_recent_order.return_date.strftime('%Y-%m-%d')
                    })
                else:
                    # Equipment found but no orders, check EquipmentEntry as fallback
                    equipment_entries = EquipmentEntry.objects.filter(
                        Q(equipment_name__iexact=equipment.name) |
                        Q(barcode__iexact=barcode)
                    ).order_by('-date')
                    
                    if equipment_entries.exists():
                        latest_entry = equipment_entries.first()
                        return JsonResponse({
                            'success': True,
                            'equipment_name': equipment.name,
                            'order_number': latest_entry.order_name,
                            'total_quantity': latest_entry.amount,
                            'date': latest_entry.date.strftime('%Y-%m-%d'),
                            'source': 'barcode_model_fallback_entry'
                        })
                    else:
                        # Equipment found but no orders
                        return JsonResponse({
                            'success': True,
                            'equipment_name': equipment.name,
                            'order_number': '',  # No order found
                            'total_quantity': 1,  # Default quantity
                            'date': '',
                            'source': 'barcode_model_no_order'
                        })
                    
            except Barcode.DoesNotExist:
                # If not found in Barcode model, fall back to EquipmentEntry search with exact match
                equipment_entries = EquipmentEntry.objects.filter(
                    Q(equipment_name__iexact=barcode) |
                    Q(barcode__iexact=barcode)
                ).order_by('-date', '-id')  # Most recent first, with ID as tiebreaker
                
                if equipment_entries.exists():
                    # Find the most recent entry
                    latest_entry = equipment_entries.first()
                    
                    # Get the most recent order for this equipment
                    most_recent_order_entry = EquipmentEntry.objects.filter(
                        equipment_name=latest_entry.equipment_name
                    ).order_by('-date', '-id').first()
                    
                    # Get total quantity for the most recent equipment/order combination
                    total_quantity = EquipmentEntry.objects.filter(
                        equipment_name=most_recent_order_entry.equipment_name,
                        order_name=most_recent_order_entry.order_name
                    ).aggregate(total=Sum('amount'))['total'] or 0
                    
                    return JsonResponse({
                        'success': True,
                        'equipment_name': most_recent_order_entry.equipment_name,
                        'order_number': most_recent_order_entry.order_name,
                        'total_quantity': total_quantity,
                        'date': most_recent_order_entry.date.strftime('%Y-%m-%d'),
                        'source': 'equipment_entry_most_recent'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Equipment not found in current data'
                    })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'An error occurred: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)


def get_qc_signoffs(request):
    """
    API endpoint to retrieve QC sign-off history
    """
    try:
        # Get recent sign-offs (limit to last 50)
        signoffs = QCSignoff.objects.all()[:50]
        
        signoffs_data = []
        for signoff in signoffs:
            signoffs_data.append({
                'id': signoff.id,
                'equipment_barcode': signoff.equipment_barcode,
                'equipment_name': signoff.equipment_name,
                'order_number': signoff.order_number,
                'inspector_name': signoff.inspector_name,
                'inspection_date': signoff.inspection_date.strftime('%Y-%m-%d'),
                'qc_status': signoff.qc_status,
                'quantity': signoff.quantity,
                'inspection_notes': signoff.inspection_notes,
                'corrective_actions': signoff.corrective_actions,
                'printer_name': signoff.printer_name,
                'print_sticker': signoff.print_sticker,
                'order_completion': signoff.order_completion,
                'completed_items': signoff.completed_items,
                'created_at': signoff.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse({
            'success': True,
            'signoffs': signoffs_data,
            'count': len(signoffs_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }, status=500)
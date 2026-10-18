from equipment_tracking_app.models import EquipmentEntry, Order, OrderEquipment

def populate_equipment_entry():
    for order in Order.objects.all():
        for order_equipment in order.order_equipments.all():
            # Extract data from Order and OrderEquipment
            equipment_name = order_equipment.equipment.equipment.name  # Get the equipment name
            order_name = order.name
            date = order.return_date
            amount = order_equipment.amount

            # Check if an EquipmentEntry already exists for this data
            equipment_entry, created = EquipmentEntry.objects.get_or_create(
                date=date,
                order_name=order_name,
                equipment_name=equipment_name,
                defaults={
                    'amount': amount,
                    'qc_area': 0,
                    'qc_by': '',
                    'qc_passed': 0,
                    'in_repair': 0,
                }
            )

            if created:
                print(f"Created EquipmentEntry for {equipment_name} in order {order_name} on {date}.")
            else:
                print(f"EquipmentEntry for {equipment_name} in order {order_name} on {date} already exists.")
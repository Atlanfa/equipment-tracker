from django.core.management.base import BaseCommand
from equipment_tracking_app.models import EquipmentEntry, Order, OrderEquipment

class Command(BaseCommand):
    help = "Populate EquipmentEntry from Order and OrderEquipment data"

    def handle(self, *args, **kwargs):
        for order in Order.objects.all():
            for order_equipment in order.order_equipments.all():
                equipment_name = order_equipment.equipment.equipment.name
                order_name = order.name
                date = order.return_date
                amount = order_equipment.amount

                equipment_entry, created = EquipmentEntry.objects.get_or_create(
                    date=date,
                    order_name=order_name,
                    barcode=order_equipment.equipment.barcode,
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
                    self.stdout.write(f"Created EquipmentEntry for {equipment_name} in order {order_name} on {date}.")
                else:
                    self.stdout.write(f"EquipmentEntry for {equipment_name} in order {order_name} on {date} already exists.")
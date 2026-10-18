from django.core.management.base import BaseCommand
from equipment_tracking_app.models import Equipment, Barcode, Location

class Command(BaseCommand):
    help = 'Populate sample equipment, barcodes, and locations for testing warehouse management'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create sample locations
        locations_data = [
            {'aile': 'A1', 'shelf': 'S1', 'row': 'R1'},
            {'aile': 'A1', 'shelf': 'S1', 'row': 'R2'},
            {'aile': 'A1', 'shelf': 'S2', 'row': 'R1'},
            {'aile': 'A2', 'shelf': 'S1', 'row': 'R1'},
            {'aile': 'A2', 'shelf': 'S2', 'row': 'R1'},
            {'aile': 'B1', 'shelf': 'S1', 'row': 'R1'},
            {'aile': 'B1', 'shelf': 'S1', 'row': 'R2'},
            {'aile': 'B2', 'shelf': 'S1', 'row': 'R1'},
        ]

        locations = []
        for loc_data in locations_data:
            location, created = Location.objects.get_or_create(**loc_data)
            locations.append(location)
            if created:
                self.stdout.write(f'Created location: {location}')

        # Create sample equipment
        equipment_data = [
            {
                'name': 'Laptop',
                'description': 'Standard office laptop for general use'
            },
            {
                'name': 'Monitor',
                'description': '24-inch LED monitor'
            },
            {
                'name': 'Projector',
                'description': 'HD projector for presentations'
            },
            {
                'name': 'Camera',
                'description': 'Digital camera for documentation'
            },
            {
                'name': 'Printer',
                'description': 'Laser printer for office use'
            },
            {
                'name': 'Scanner',
                'description': 'Document scanner'
            },
            {
                'name': 'Tablet',
                'description': 'Tablet for mobile work'
            },
            {
                'name': 'Microphone',
                'description': 'Wireless microphone system'
            },
        ]

        equipment_objects = []
        for eq_data in equipment_data:
            equipment, created = Equipment.objects.get_or_create(
                name=eq_data['name'],
                defaults={'description': eq_data['description']}
            )
            equipment_objects.append(equipment)
            if created:
                self.stdout.write(f'Created equipment: {equipment.name}')

        # Create sample barcodes with ASL prefix and alphanumeric codes
        barcode_data = [
            {'equipment_name': 'Laptop', 'barcodes': ['ASL001LP', 'ASL002LP', 'ASL003LP', 'LAP001', '123456789012']},
            {'equipment_name': 'Monitor', 'barcodes': ['ASL001MN', 'ASL002MN', 'MON001', '234567890123']},
            {'equipment_name': 'Projector', 'barcodes': ['ASL001PJ', 'PROJ001', '345678901234']},
            {'equipment_name': 'Camera', 'barcodes': ['ASL001CM', 'ASL002CM', 'CAM001', '456789012345']},
            {'equipment_name': 'Printer', 'barcodes': ['ASL001PR', 'PRT001', '567890123456']},
            {'equipment_name': 'Scanner', 'barcodes': ['ASL001SC', 'SCN001', '678901234567']},
            {'equipment_name': 'Tablet', 'barcodes': ['ASL001TB', 'ASL002TB', 'ASL003TB', 'TAB001', '789012345678']},
            {'equipment_name': 'Microphone', 'barcodes': ['ASL001MC', 'ASL002MC', 'MIC001', '890123456789']},
        ]

        for bc_data in barcode_data:
            try:
                equipment = Equipment.objects.get(name=bc_data['equipment_name'])
                for barcode_value in bc_data['barcodes']:
                    barcode, created = Barcode.objects.get_or_create(
                        equipment=equipment,
                        barcode=barcode_value
                    )
                    if created:
                        self.stdout.write(f'Created barcode: {barcode.barcode} for {equipment.name}')
            except Equipment.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Equipment {bc_data["equipment_name"]} not found')
                )

        # Assign locations to equipment
        location_assignments = [
            {'equipment_name': 'Laptop', 'location_indices': [0, 1, 2]},
            {'equipment_name': 'Monitor', 'location_indices': [1, 3]},
            {'equipment_name': 'Projector', 'location_indices': [4]},
            {'equipment_name': 'Camera', 'location_indices': [5, 6]},
            {'equipment_name': 'Printer', 'location_indices': [2]},
            {'equipment_name': 'Scanner', 'location_indices': [3]},
            {'equipment_name': 'Tablet', 'location_indices': [0, 4, 7]},
            {'equipment_name': 'Microphone', 'location_indices': [5, 6]},
        ]

        for assignment in location_assignments:
            try:
                equipment = Equipment.objects.get(name=assignment['equipment_name'])
                for loc_index in assignment['location_indices']:
                    if loc_index < len(locations):
                        equipment.locations.add(locations[loc_index])
                        self.stdout.write(
                            f'Assigned {equipment.name} to location {locations[loc_index]}'
                        )
            except Equipment.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Equipment {assignment["equipment_name"]} not found')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed successfully!')
        )
        self.stdout.write(
            self.style.SUCCESS('You can now test the warehouse management system.')
        )

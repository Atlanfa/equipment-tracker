import os
from django.core.management.base import BaseCommand
from equipment_tracking_app.utils.import_csv import process_csv_file  # Move the script to a utils.py file

class Command(BaseCommand):
    help = "Import order returns from all CSV files in the order_data directory"

    def add_arguments(self, parser):
        parser.add_argument(
            '--directory',
            type=str,
            default='/home/apex/Documents/dashboardV2/equipment_tracking_project/order_data',
            help="Path to the directory containing CSV files (default: equipment_tracking_project/order_data)"
        )

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']

        # Check if the directory exists
        if not os.path.isdir(directory):
            self.stderr.write(f"Error: Directory '{directory}' does not exist.")
            return

        # Iterate through all files in the directory
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)

            # Process only CSV files
            if file_name.endswith('.csv'):
                self.stdout.write(f"Processing file: {file_name}")
                try:
                    process_csv_file(file_path)
                    self.stdout.write(f"Successfully processed: {file_name}")
                except Exception as e:
                    self.stderr.write(f"Error processing {file_name}: {e}")

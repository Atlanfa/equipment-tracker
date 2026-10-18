import os
import time
from subprocess import call

# Path to the directory containing CSV files
CSV_DIRECTORY = '/home/apex/Documents/dashboardV2/equipment_tracking_project/order_data'

# Path to the file storing the last modification time
LAST_RUN_FILE = '/home/apex/Documents/dashboardV2/last_run_timestamp.txt'

def get_last_run_time():
    """Retrieve the last run timestamp from the file."""
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as file:
            return float(file.read().strip())
    return 0

def update_last_run_time():
    """Update the last run timestamp in the file."""
    with open(LAST_RUN_FILE, 'w') as file:
        file.write(str(time.time()))

def has_new_files(directory, last_run_time):
    """Check if there are new or modified files in the directory since the last run."""
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name.endswith('.csv') and os.path.isfile(file_path):
            if os.path.getmtime(file_path) > last_run_time:
                return True
    return False

def main():
    last_run_time = get_last_run_time()

    # Check if there are new or modified files
    if has_new_files(CSV_DIRECTORY, last_run_time):
        print("New files detected. Running tasks...")

        # Run the import_order_returns command
        call(['python3', '/home/apex/Documents/dashboardV2/equipment_tracking_project/manage.py', 'import_order_returns'])

        # Run the populate_equipment_entry command
        call(['python3', '/home/apex/Documents/dashboardV2/equipment_tracking_project/manage.py', 'populate_equipment_entry'])

        # Update the last run timestamp
        update_last_run_time()
    else:
        print("No new files detected. Skipping tasks.")

if __name__ == '__main__':
    main()

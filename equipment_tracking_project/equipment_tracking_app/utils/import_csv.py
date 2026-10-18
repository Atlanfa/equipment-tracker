import csv
from datetime import datetime
from equipment_tracking_app.models import Equipment, Barcode, Order, OrderEquipment

def process_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        return_date = None
        i =0
        # Extract the return date from the 6 row
        # return date is always on row 6 column 6
        for row in reader:
            if len(row) > 5 and row[5].strip():
                return_date_raw = row[5].strip()
                return_date = extract_return_date(return_date_raw)
                if return_date:
                    print(f"Extracted return date: {return_date}")
                    break
        else:
            print("No valid return date found in the CSV file.")
            return
        file.seek(0)  # Reset file pointer to the beginning
        next(reader)  # Skip the header row again
        # Process each row in the CSV file
        
        file_name= file_path.split("/")[-1].replace(".csv","")
        file_name = file_name[:file_name.rfind("-")-1].replace("-","")
        # Check if the file name is empty
        print(f"File name: {file_name}")
        



        
        for row_number, row in enumerate(reader, start=2):  # Start from row 2 to account for the header
            try:
                
                # Validate row length
                if len(row) < 7:
                    print(f"Skipping row {row_number}: Not enough columns.")
                    continue

                # Print row data for debugging
                print(f"Row {row_number} data: {row}")

                # Extract and validate data
                equipment_name = row[3].strip() if row[3].strip() else None  # Column 4: Equipment name (Description)
                amount = int(row[2].strip()) if row[2].strip().isdigit() else None  # Column 3: Amount
                barcode_value = row[6].strip() if row[6].strip() else row[5].strip() if row[5].strip() else None  # Column 7: Barcode
                return_date_raw = row[5].strip() if row[5].strip() else None  # Column 6: Return date

                # Skip rows with missing critical data
                if not equipment_name or not amount or not barcode_value:
                    print(f"Skipping row {row_number}: Missing critical data. Equipment name: {equipment_name}, Amount: {amount}, Barcode: {barcode_value}")
                    continue

                
                    

                # Check if the equipment exists in the database
                try:
                    equipment = Equipment.objects.get(name=equipment_name)
                except Equipment.DoesNotExist:
                    
                    continue

                # Create or get the order
                order, _ = Order.objects.get_or_create(
                    name=file_name,
                    return_date=return_date
                )
                barcode, created = Barcode.objects.get_or_create(
                    equipment=equipment,
                    barcode=barcode_value
                )
                # Create or get the OrderEquipment entry
                order_equipment, _ = OrderEquipment.objects.get_or_create(
                    order=order,
                    equipment=barcode,
                    defaults={'amount': amount}
                )

                # Create the barcode if it doesn't exist
                
                if created:
                    print(f"Row {row_number}: Created new barcode: {barcode_value} for equipment: {equipment_name}")

                

                print(f"Row {row_number}: Processed equipment: {equipment_name}, amount: {amount}, barcode: {barcode_value}, return date: {return_date}")
                
                
            except Exception as e:
                print(f"Error processing row {row_number}: {e}")


def extract_return_date(raw_string):
    """
    Extract the return date from the raw string in the format:
    "Delivery Date:2025-05-05Return Date:2025-05-09 Delivery Via:CustomerReturn Via:Customer"
    """
    try:
        # Find the "Return Date" substring and extract the date
        start = raw_string.find("Return Date:") + len("Return Date:")
        end = raw_string.find(" ", start)
        return_date_str = raw_string[start:end] if end != -1 else raw_string[start:]
        return datetime.strptime(return_date_str, '%Y-%m-%d').date()
    except Exception as e:
        print(f"Error extracting return date from '{raw_string}': {e}")
        return None
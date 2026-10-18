from django.db import models
import datetime

class EquipmentEntry(models.Model):
    day = models.CharField(max_length=20, editable=False)  # Make it non-editable
    date = models.DateField()
    order_name = models.CharField(max_length=100)
    equipment_name = models.CharField(max_length=100)
    amount = models.IntegerField()
    qc_area = models.IntegerField(default=0)  # Changed to IntegerField
    qc_by = models.CharField(max_length=100, blank=True)
    qc_passed = models.IntegerField(default=0)  # Changed to IntegerField
    in_repair = models.IntegerField(default=0)  # Changed to IntegerField
    barcode = models.CharField(max_length=50, blank=True)  # Added barcode field

    def save(self, *args, **kwargs):
        # Automatically set the day of the week based on the date
        if self.date:
            self.day = self.date.strftime('%A')  # Get the full name of the day (e.g., "Monday")

        # Ensure qc_area, qc_passed, and in_repair do not exceed the amount
        if self.amount:
            self.qc_area = min(self.qc_area, self.amount)
            self.qc_passed = min(self.qc_passed, self.amount)
            self.in_repair = min(self.in_repair, self.amount)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.equipment_name} - {self.order_name} ({self.date})'


class Location(models.Model):
    aile = models.CharField(max_length=100)  # Name of the aisle
    shelf = models.CharField(max_length=100)  # Name of the shelf
    row = models.CharField(max_length=100)  # Name of the row

    def __str__(self):
        return f'{self.aile} - {self.shelf} - {self.row}'
    

class Note(models.Model):
    content = models.TextField()  # The content of the note
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the note was created
    highlight_color = models.CharField(max_length=7, default="#ffff00")  # Default highlight color (yellow)
    done = models.BooleanField(default=False)  # Indicates if the note is marked as "Done"

    
class QCStaff(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique name for each equipment type
    # I need to add a range of Locations for each equipment there could be several entries of location per one type of equipment
    locations = models.ManyToManyField(Location, related_name='equipments', blank=True)  # Many
    description = models.TextField(blank=True, null=True)  # Optional description of the equipment

    def __str__(self):
        return self.name
    
    

class Barcode(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='barcodes')  # Link to Equipment
    barcode = models.CharField(max_length=50, unique=True)  # Unique barcode for each entry
    assigned_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the barcode was assigned

    def __str__(self):
        return f'{self.equipment.name} - {self.barcode}'

class Order(models.Model):
    name = models.CharField(max_length=100)  # Name of the order
    return_date = models.DateField()  # Date the order returned to the warehouse

    def __str__(self):
        return self.name


class OrderEquipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_equipments')  # Link to Order
    equipment = models.ForeignKey(Barcode, on_delete=models.CASCADE, related_name='order_equipments')  # Link to Barcode
    amount = models.IntegerField()  # Amount of this equipment in the order

    def __str__(self):
        return f'{self.equipment.equipment.name} - {self.order.name} ({self.amount})'


class QCSignoff(models.Model):
    QC_STATUS_CHOICES = [
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('partial', 'Partial Pass'),
        ('pending', 'Pending Review'),
    ]
    
    ORDER_COMPLETION_CHOICES = [
        ('all', 'All Items Completed'),
        ('partial', 'Partial Items Completed'),
    ]
    
    # Equipment information
    equipment_barcode = models.CharField(max_length=100)
    equipment_name = models.CharField(max_length=100, blank=True)  # Auto-filled from lookup
    order_number = models.CharField(max_length=100)
    
    # Inspector information
    inspector_name = models.CharField(max_length=100)
    inspection_date = models.DateField()
    
    # QC details
    qc_status = models.CharField(max_length=20, choices=QC_STATUS_CHOICES, default='passed')
    quantity = models.IntegerField()
    inspection_notes = models.TextField(default="All units passed visual inspection and functionality tests.")
    corrective_actions = models.TextField(blank=True)
    
    # Order completion tracking
    order_completion = models.CharField(max_length=20, choices=ORDER_COMPLETION_CHOICES, default='all')
    completed_items = models.JSONField(default=list, blank=True)  # Store array of barcodes for partial completion
    
    # Printing information
    printer_name = models.CharField(max_length=100)
    print_sticker = models.BooleanField(default=True)
    use_default_notes = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "QC Sign-off"
        verbose_name_plural = "QC Sign-offs"
    
    def __str__(self):
        return f"{self.equipment_name or 'Equipment'} - Order #{self.order_number} - {self.qc_status} ({self.inspection_date})"

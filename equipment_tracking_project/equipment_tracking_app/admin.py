from django.contrib import admin
from .models import EquipmentEntry, Note, QCStaff, Equipment, Location, QCSignoff, Barcode

admin.site.register(EquipmentEntry)  # Register the EquipmentEntry model with the admin site

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'highlight_color', 'done')
    list_filter = ('done',)
    search_fields = ('content',)

# Register the QCStaff model
@admin.register(QCStaff)
class QCStaffAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name field in the admin list view
    search_fields = ('name',)  # Add a search bar for the name field

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'equipment', 'assigned_at')
    search_fields = ('barcode', 'equipment__name')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('aile', 'shelf', 'row')
    search_fields = ('aile', 'shelf', 'row')

@admin.register(QCSignoff)
class QCSignoffAdmin(admin.ModelAdmin):
    list_display = (
        'equipment_name', 
        'order_number', 
        'inspector_name', 
        'qc_status', 
        'inspection_date',
        'quantity',
        'print_sticker',
        'created_at'
    )
    list_filter = ('qc_status', 'inspection_date', 'print_sticker', 'order_completion')
    search_fields = ('equipment_barcode', 'equipment_name', 'order_number', 'inspector_name', 'printer_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Equipment Information', {
            'fields': ('equipment_barcode', 'equipment_name', 'order_number')
        }),
        ('Inspector Information', {
            'fields': ('inspector_name', 'inspection_date')
        }),
        ('QC Details', {
            'fields': ('qc_status', 'quantity', 'inspection_notes', 'corrective_actions')
        }),
        ('Order Completion', {
            'fields': ('order_completion', 'completed_items')
        }),
        ('Printing', {
            'fields': ('printer_name', 'print_sticker', 'use_default_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

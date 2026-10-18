from django.contrib import admin
from django.urls import path
from equipment_tracking_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.equipment_tracking_view, name='equipment_tracking'),
    path('update-entry/', views.update_equipment_entry, name='update_entry'),
    path('add-note/', views.add_note_view, name='add_note'),
    path('api/search-equipment/', views.search_equipment_view, name='search_equipment'),
    path('api/qc-signoff/', views.qc_signoff_view, name='qc_signoff'),
    path('api/lookup-equipment/', views.lookup_equipment_by_barcode, name='lookup_equipment'),
    path('api/qc-signoffs/', views.get_qc_signoffs, name='get_qc_signoffs'),
]
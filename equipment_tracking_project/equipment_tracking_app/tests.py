from django.test import TestCase
from django.urls import reverse

class EquipmentTrackingViewTests(TestCase):
    def test_equipment_tracking_view_status_code(self):
        response = self.client.get(reverse('equipment_tracking'))
        self.assertEqual(response.status_code, 200)

    def test_equipment_tracking_view_template(self):
        response = self.client.get(reverse('equipment_tracking'))
        self.assertTemplateUsed(response, 'equipment_tracking.html')

    def test_equipment_tracking_view_contains_correct_html(self):
        response = self.client.get(reverse('equipment_tracking'))
        self.assertContains(response, 'Equipment QC Tracking')
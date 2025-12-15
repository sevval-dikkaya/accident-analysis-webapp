from django.test import TestCase
from django.urls import reverse
from .models import Accidents, Vehicles
import datetime

class AccidentModelTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicles.objects.create(
            manufacturer_name="TestName",
            make="TestMake",
            model="TestModel",
            vehicle_year=2022
        )
        self.accident = Accidents.objects.create(
            date_of_accident=datetime.date(2023, 1, 1),
            damage_type="minor",
            address_accident=12345
        )
        self.accident.vehicles.add(self.vehicle)

    def test_accident_creation(self):
        self.assertEqual(self.accident.damage_type, "minor")
        self.assertEqual(self.accident.vehicles.count(), 1)
        self.assertEqual(str(self.accident), f"Accident {self.accident.id} - 2023-01-01")

class AccidentViewTest(TestCase):
    def setUp(self):
        self.url = reverse('accident_list')

    def test_accident_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accident_analysis/accident_list.html')


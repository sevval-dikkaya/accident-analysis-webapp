from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
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

class AccidentAPITest(APITestCase):
    def setUp(self):
        self.vehicle = Vehicles.objects.create(
            manufacturer_name="Toyota",
            make="Camry",
            model="LE",
            vehicle_year=2020
        )
        self.url = '/api/accidents/'

    def test_create_accident_validation(self):
        """
        Test that creating an accident without a date returns a 400 Bad Request
        instead of a 500 Server Error.
        """
        data = {
            'damage_type': 'minor',
            'address_accident': '12345'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_of_accident', response.data)

    def test_create_accident_with_vehicles(self):
        """
        Test that we can associate vehicles when creating an accident via API.
        """
        data = {
            'date_of_accident': '2023-01-01',
            'damage_type': 'minor',
            'address_accident': '12345',
            'vehicles': [self.vehicle.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        accident = Accidents.objects.get(id=response.data['id'])
        self.assertEqual(accident.vehicles.count(), 1)
        self.assertEqual(accident.vehicles.first(), self.vehicle)



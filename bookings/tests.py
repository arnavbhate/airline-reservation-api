from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from flights.models import Flight
from airports.models import Airport
from datetime import date

class BookingTests(TestCase):

    def setUp(self):
        # Create test airports
        self.airport1 = Airport.objects.create(code="JFK", name="John F. Kennedy")
        self.airport2 = Airport.objects.create(code="LAX", name="Los Angeles International")
        
        # Create test flight
        self.flight = Flight.objects.create(
            flight_no="AA123",
            departure_airport=self.airport1,
            arrival_airport=self.airport2,
            departure_time="10:00",
            arrival_time="13:00",
            economy_class_seats=100,
            economy_class_price=200,
            business_class_seats=50,
            business_class_price=500,
            first_class_seats=10,
            first_class_price=1000
        )
        
        # Set up API client
        self.client = APIClient()
        
    def test_create_booking(self):
        # Test creating a booking
        url = '/api/bookings/create/'
        data = {
            "flight_code": self.flight.flight_no,
            "booking_class": "E",
            "date": str(date.today()),
            "list_of_passengers": [
                {"first_name": "John", "last_name": "Doe", "title": "Mr.", "age": 30}
            ]
        }
        
        response = self.client.post(url, data, format='json')
        
        # Assert the response is 201 created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('pnr', response.data)
        self.assertEqual(response.data['flight_code'], self.flight.flight_no)
        self.assertEqual(response.data['booking_class'], "E")
        
    def test_create_booking_incomplete_fields(self):
        # Test creating a booking with missing fields
        url = '/api/bookings/create/'
        data = {
            "flight_code": self.flight.flight_no,
            "booking_class": "E",
            "date": str(date.today()),
        }  # Missing list_of_passengers
        
        response = self.client.post(url, data, format='json')
        
        # Assert the response is 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Incomplete Fields")
        
    def test_view_booking(self):
        # Test viewing a booking
        create_url = '/api/bookings/create/'
        create_data = {
            "flight_code": self.flight.flight_no,
            "booking_class": "E",
            "date": str(date.today()),
            "list_of_passengers": [
                {"first_name": "Jane", "last_name": "Smith", "title": "Ms.", "age": 25}
            ]
        }
        
        # Create the booking
        create_response = self.client.post(create_url, create_data, format='json')
        pnr = create_response.data['pnr']
        
        # Get the booking using its PNR
        view_url = f'/api/bookings/{pnr}/'
        response = self.client.get(view_url)
        
        # Assert the response is 202 accepted
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['pnr'], pnr)
        self.assertEqual(response.data['flight_code'], self.flight.flight_no)
        
    def test_update_booking(self):
        # Test updating a booking
        create_url = '/api/bookings/create/'
        create_data = {
            "flight_code": self.flight.flight_no,
            "booking_class": "E",
            "date": str(date.today()),
            "list_of_passengers": [
                {"first_name": "Mike", "last_name": "Jordan", "title": "Mr.", "age": 35}
            ]
        }
        
        # Create the booking
        create_response = self.client.post(create_url, create_data, format='json')
        pnr = create_response.data['pnr']
        
        # Update the booking with new passenger data
        update_url = f'/api/bookings/{pnr}/update/'
        update_data = {
            "flight_code": self.flight.flight_no,
            "booking_class": "B",  # Changing booking class
            "date": str(date.today()),
        }
        
        response = self.client.put(update_url, update_data, format='json')
        
        # Assert the response is 202 accepted
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['booking_class'], "B")
        
    def test_delete_booking(self):
        # Test deleting a booking
        create_url = '/api/bookings/create/'
        create_data = {
            "flight_code": self.flight.flight_no,
            "booking_class": "E",
            "date": str(date.today()),
            "list_of_passengers": [
                {"first_name": "Mike", "last_name": "Jordan", "title": "Mr.", "age": 35}
            ]
        }
        
        # Create the booking
        create_response = self.client.post(create_url, create_data, format='json')
        pnr = create_response.data['pnr']
        
        # Delete the booking
        delete_url = f'/api/bookings/{pnr}/delete/'
        response = self.client.delete(delete_url)
        
        # Assert the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "deletion successful")
        
        # Try to view the booking after deletion (should return 404)
        view_url = f'/api/bookings/{pnr}/'
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

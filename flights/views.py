from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Flight
from .serializers import FlightSerializer

# List flights with optional filters
@api_view(['GET'])
def list_flights(request):
    flights = Flight.objects.all()
    
    # Extract filter parameters from request
    departure_airport = request.GET.get('departure_airport')
    arrival_airport = request.GET.get('arrival_airport')

    # Apply filters if parameters are provided
    if departure_airport:
        flights = flights.filter(departure_airport__code=departure_airport.upper())
    if arrival_airport:
        flights = flights.filter(arrival_airport__code=arrival_airport.upper())
    
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve a single flight by flight_no
@api_view(['GET'])
def retrieve_flight(request, flight_no):
    flight = get_object_or_404(Flight, flight_no=flight_no)
    serializer = FlightSerializer(flight)
    return Response(serializer.data, status=status.HTTP_200_OK)


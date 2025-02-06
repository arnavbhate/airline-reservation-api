from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Flight
from .serializers import FlightSerializer

# List all flights
@api_view(['GET'])
def list_flights(request):
    flights = Flight.objects.all()
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve a single flight by flight_no
@api_view(['GET'])
def retrieve_flight(request, flight_no):
    flight = get_object_or_404(Flight, flight_no=flight_no)
    serializer = FlightSerializer(flight)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Update seat count when a booking is made
@api_view(['PATCH'])
def update_seat_count(request, flight_no):
    flight = get_object_or_404(Flight, flight_no=flight_no)
    seat_updates = request.data

    valid_seat_types = ["economy_class_seats", "business_class_seats", "first_class_seats"]

    for seat_type, count in seat_updates.items():
        if seat_type in valid_seat_types and isinstance(count, int) and count >= 0:
            setattr(flight, seat_type, count)
        else:
            return Response({"error": f"Invalid seat update for {seat_type}"}, status=status.HTTP_400_BAD_REQUEST)

    flight.save()
    return Response({"message": "Seat count updated successfully"}, status=status.HTTP_200_OK)

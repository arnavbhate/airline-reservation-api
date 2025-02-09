from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Airport
from .serializers import AirportSerializer

# List all airports
@api_view(['GET'])
def list_airports(request):
    airports = Airport.objects.all()
    serializer = AirportSerializer(airports, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve a single airport by code
@api_view(['GET'])
def retrieve_airport(request, code):
    airport = get_object_or_404(Airport, code=code.upper())  # Case-insensitive lookup
    serializer = AirportSerializer(airport)
    return Response(serializer.data, status=status.HTTP_200_OK)

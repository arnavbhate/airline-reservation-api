from django.shortcuts import render
from .models import Booking
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import uuid
from .serializers import BookingSerializer

#post request to add entry
@api_view(['POST'])
def create_booking(req):
    #extract given data
    data = req.data
    #assign from given data
    flight_code = data.get("flight_code")
    booking_class = data.get("booking_class")
    date = data.get("date")
    list_of_passengers = data.get("list_of_passengers", [])
    #make sure not empty
    if not flight_code or not booking_class or not date or (list_of_passengers == []):
        return Response({"error" : "Incomplete Fields"}, status=status.HTTP_400_BAD_REQUEST)
    #generate pnr
    pnr = str(uuid.uuid4())[:6].upper()
    #assign pnr
    data["pnr"] = pnr
    #check and save or raise error
    serializer = BookingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
#get request to view entry
@api_view(['GET'])
def view_booking(req, pnr):
    #retrieve entry and then return entry
    booking = get_object_or_404(Booking, pnr=pnr)
    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

#put request to update entry (assuming since put, every field is given again instead of just the update fields)
@api_view(['PUT'])
def update_booking(req, pnr):
    #extract data
    data = req.data
    #retrieve required entry
    booking = get_object_or_404(Booking, pnr=pnr)
    #modify
    serializer = BookingSerializer(booking, data=data)
    #check then update or raise error
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def delete_booking(req, pnr):
    #find required entry
    booking = get_object_or_404(Booking, pnr=pnr)
    #delete entry
    booking.delete()
    #return response
    return Response({"message" : "deletion successful"}, status=status.HTTP_200_OK)

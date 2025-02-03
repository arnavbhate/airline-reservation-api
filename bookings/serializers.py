from rest_framework import serializers
from .models import Booking, Flight
from datetime import date
from django.db.models import Sum


#checking if each passenger record is ok
class PassengerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    title = serializers.ChoiceField(choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.'), ('Dr.', 'Dr.')])
    date_of_birth = serializers.DateField()

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("You weren't born in the future!")
        return value


class BookingSerializer(serializers.ModelSerializer):
#defined to get attribute names for later
    classes = {
            'E' : 'economy_class_seats',
            'F' : 'first_class_seats',
            'B' : 'business_class_seats'
        }

    #checking basic fields
    booking_class = serializers.ChoiceField(choices=Booking.BookingClasses.choices)
    flight_code = serializers.CharField(max_length=6)
    date = serializers.DateField()
    list_of_passengers = PassengerSerializer(many=True)
    
    #making sure passenger list not empty
    def validate_list_of_passengers(self, value):
        if not value:  # checks if the list is empty
            raise serializers.ValidationError("Can't have zero passengers")
        return value
    #making sure flight isnt booked for the past
    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("You can't book a flight for the past!")
        return value

    #making sure enough seats are avaiable
    def validate(self, data):
        #calc the no of seats booked
        data['seats_booked'] = len(data.get('list_of_passengers'))
        #get basic info
        flight = Flight.objects.get(flight_no=data.get('flight_code'))
        booking_class = data.get('booking_class')
        no_of_seats = len(data.get('list_of_passengers'))
        date = data.get('date')
        #check if enough seats are available
        if getattr(flight, self.classes.get(booking_class)) < no_of_seats + Booking.objects.filter(flight_code=flight, booking_class=booking_class, date=date).aggregate(Sum('seats_booked'))['seats_booked__sum']:
            raise serializers.ValidationError("Not enough seats are available")

        return data

    #updates for put request
    def update(self, old_data, new_data):
        #preliminary check
        list_of_passengers = new_data.get('list_of_passengers')
        if old_data.get('list_of_passengers') != list_of_passengers:
            raise serializers.ValidationError("Can't change passenger info")
        #get basic info
        new_flight = Flight.objects.get(flight_no=old_data.get('flight_code'))
        new_booking_class = new_data.get('booking_class')
        no_of_seats = len(list_of_passengers)
        date = new_data.get('date')

        #checking if enough no of seats are available for change in new flight
        if getattr(new_flight, self.classes.get(new_booking_class)) < no_of_seats + Booking.objects.filter(flight_code=new_flight, booking_class=new_booking_class, date=date).aggregate(Sum('seats_booked'))['seats_booked__sum']:
            #raise error if not
            raise serializers.ValidationError("Not enough available seats.")
        
        return super().update(old_data, new_data)
    

    class Meta:
        model = Booking
        fields = '__all__'

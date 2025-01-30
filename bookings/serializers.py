from rest_framework import serializers
from .models import Booking, Flight
from datetime import date


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
    list_of_passengers = PassengerSerializer(many=True)
    
    #making sure passenger list not empty
    def validate_list_of_passengers(self, value):
        if not value:  # checks if the list is empty
            raise serializers.ValidationError("Can't have zero passengers")
        return value

    #making sure enough seats are avaiable
    def validate(self, data):
        #get basic info
        flight = Flight.objects.get(flight_no=data.get('flight_code'))
        booking_class = self.classes.get(data.get('booking_class'))
        no_of_seats = len(data.get('list_of_passengers'))
        #check if enough seats are available
        if getattr(flight, booking_class) <= no_of_seats:
            raise serializers.ValidationError("Not enough seats are available")

        return data
    #creating entry and updating no of seats left
    def create(self, validated_data):
        #get basic info
        flight = Flight.objects.get(flight_no=validated_data.get('flight_code'))
        booking_class = self.classes.get(validated_data.get('booking_class'))
        no_of_seats = len(validated_data.get('list_of_passengers'))
        #update no of seats
        setattr(flight, booking_class, getattr(flight, booking_class) - no_of_seats)

        flight.save()

        return super().create(validated_data)
    #updates for put request
    def update(self, old_data, new_data):
        #get basic info
        old_flight = Flight.objects.get(flight_no=new_data.get('flight_code'))
        new_flight = Flight.objects.get(flight_no=old_data.get('flight_code'))
        new_booking_class = self.classes.get(new_data.get('booking_class'))
        old_booking_class = self.classes.get(new_data.get('booking_class'))
        new_no_of_seats = len(new_data.get('list_of_passengers'))
        old_no_of_seats = len(old_data.get('list_of_passengers'))
        #for control logic used later
        enough = True

        #reassign seats that arent needed anymore
        setattr(old_flight, old_booking_class, getattr(old_flight, old_booking_class) + old_no_of_seats)
        #checking if enough no of seats are available for change in new flight
        if getattr(new_flight, new_booking_class) <= new_no_of_seats:
            enough = False
        #if not enough seats are available
        if not enough:
            #undo changes in old flight
            setattr(old_flight, old_booking_class, getattr(old_flight, old_booking_class) - old_no_of_seats)
            #and then raise error
            raise serializers.ValidationError("Not enough available seats.")
        #else update no of seats in new flight
        setattr(new_flight, new_booking_class, getattr(new_flight, new_booking_class) - new_no_of_seats)
        #save
        old_flight.save()
        new_flight.save()

        return super().update(old_data, new_data)
    

    class Meta:
        model = Booking
        fields = '__all__'

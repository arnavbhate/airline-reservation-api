from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

    def validate(self, data):
        if data.get("departure_airport") == data.get("arrival_airport"):
            raise serializers.ValidationError("Departure and arrival airports must be different.")
        if data.get("economy_class_seats") < 0 or data.get("business_class_seats") < 0 or data.get("first_class_seats") < 0:
            raise serializers.ValidationError("Seat count cannot be negative.")
        if data.get("economy_class_price") <= 0 or data.get("business_class_price") <= 0 or data.get("first_class_price") <= 0:
            raise serializers.ValidationError("Ticket price must be greater than zero.")
        return data

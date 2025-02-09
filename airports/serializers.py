from rest_framework import serializers
from .models import Airport

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

    def validate_code(self, value):
        if len(value) != 3 or not value.isalpha():
            raise serializers.ValidationError("Airport code must be exactly 3 alphabetic characters.")
        return value

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Airport name must be at least 2 characters long.")
        return value

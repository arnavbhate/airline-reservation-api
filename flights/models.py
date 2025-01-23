from django.db import models
from airports.models import Airport

# Create your models here.
class Flight(models.Model):
    flight_no = models.CharField(max_length=7,primary_key=True)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_airport')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_airport')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    economy_class_seats = models.IntegerField()
    economy_class_price = models.PositiveIntegerField()
    business_class_seats = models.IntegerField()
    business_class_price = models.PositiveIntegerField()
    first_class_seats = models.IntegerField()
    first_class_price = models.PositiveIntegerField()

    def __str__(self):
        return f"Flight {self.flight_no}"

from django.db import models

# Create your models here.
class Flight_record(models.Model):
    flight_id = models.CharField(max_length=15,unique=True)
    departure_airport = models.ForeignKey(max_length=100)
    arrival_airport = models.ForeignKey(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    economy_seats = models.IntegerField()
    economy_price = models.PositiveIntegerField()
    business_seats = models.IntegerField()
    business_price = models.PositiveIntegerField()
    first_class_seats = models.IntegerField()
    first_class_price = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Flight {self.flight_id}"
    

    

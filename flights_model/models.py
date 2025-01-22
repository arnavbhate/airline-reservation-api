from django.db import models

# Create your models here.
class Flight_record(models.Model):
    flight_id = models.CharField(max_length=15,unique=True)
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    economy_seats = models.IntegerField()
    business_seats = models.IntegerField()
    first_class_seats = models.IntegerField()
    
    def __str__(self):
        return f"Flight {self.flight_id}"
    

    

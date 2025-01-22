from django.db import models
from flights.models import Flight

class Booking(models.Model):

    class BookingClasses(models.TextChoices):
        Economy = 'E', 'Economy'
        FirstClass = 'F', 'First Class'
        BusinessClass = 'B', 'Business Class'

    booking_class = models.CharField(
        max_length=1,
        choices=BookingClasses.choices,
        default=BookingClasses.Economy,
    )

    pnr = models.CharField(max_length=6, primary_key=True)
    flight_code = models.ForeignKey(Flight, on_delete=models.CASCADE)
    date = models.DateField()
    list_of_passengers = models.JSONField(default=list) #can add data like age, name etc from front end
    
    def __str__(self):
        return "Booking of" + self.pnr
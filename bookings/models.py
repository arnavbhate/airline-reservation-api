from django.db import models
from flights.models import Flight

class Booking(models.Model):
    flight_code = models.ForeignKey(Flight, on_delete=models.CASCADE)
    date = models.DateField()
    list_of_passengers = models.JSONField(default=list) #can add pnr, and other data like age, name etc from front end?
    
    def __str__(self):
        return "Bookings of" + self.pnr
from django.db import models
from flights.models import Flight


class Booking(models.Model):

    class BookingClasses(models.TextChoices):
        EconomyClass = "E", "Economy Class"
        FirstClass = "F", "First Class"
        BusinessClass = "B", "Business Class"

    booking_class = models.CharField(
        max_length=1,
        choices=BookingClasses.choices,
        default=BookingClasses.EconomyClass,
    )

    pnr = models.CharField(max_length=6, primary_key=True)
    flight_no = models.ForeignKey(Flight, on_delete=models.CASCADE)
    date = models.DateField()
    list_of_passengers = models.JSONField(
        default=list
    )  # can add data like age, name etc from front end
    seats_booked = models.IntegerField(default=0)  # to count the no. of seats booked

    def __str__(self):
        return "Booking of" + self.pnr

from django.contrib import admin

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_id', 'departure_airpor', 'arrival_arrival', 'departure_time', 'arrival_time', 'economy_seat','business_seat','first_class_seat')
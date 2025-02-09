from django.urls import path
from .views import list_flights, retrieve_flight, update_seat_count

urlpatterns = [
    path('', list_flights, name='list_flights'),  # List & Filter Flights
    path('<str:flight_no>/', retrieve_flight, name='retrieve_flight'),  # Get Flight
]

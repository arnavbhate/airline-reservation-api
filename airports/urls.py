from django.urls import path
from .views import list_airports, retrieve_airport

urlpatterns = [
    path('', list_airports, name='list_airports'),  # List Airports
    path('<str:code>/', retrieve_airport, name='retrieve_airport'),  # Get Airport Details
]

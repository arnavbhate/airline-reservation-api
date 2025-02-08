from django.urls import path
from .views import create_booking, view_booking, update_booking, delete_booking

urlpatterns = [
    path('create/', create_booking, name='create-booking'),  #post
    path('<str:pnr>/', view_booking, name='view-booking'),    #get
    path('<str:pnr>/update/', update_booking, name='update-booking'),  #put
    path('<str:pnr>/delete/', delete_booking, name='delete-booking'),  #delete
]

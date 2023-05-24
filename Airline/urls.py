from django.urls import path
from . import views

urlpatterns = [
    path('reserve/<str:det_from>TO<str:det_to>',views.flight_booking, name="flight"),
]


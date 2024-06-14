from django.contrib import admin
from .models import Flights, Flight_Reserve, Offer, Booking

# Register your models here.
admin.site.register(Flights)
admin.site.register(Flight_Reserve)
admin.site.register(Offer)
admin.site.register(Booking)
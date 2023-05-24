from django.contrib import admin
from .models import Flights, Flight_Reserve
# Register your models here.
admin.site.register(Flights)
admin.site.register(Flight_Reserve)
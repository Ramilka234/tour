from django import forms
from .models import Flight_Reserve

class FlightForm(forms.ModelForm):

    class Meta:
        model = Flight_Reserve
        fields = ['Flight_Info', 'tickets']

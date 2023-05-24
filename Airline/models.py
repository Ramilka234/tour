from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Flights(models.Model):
    Companies = (
        ('EGA', 'Egypt Air'),
        ('NIA', 'Nile Air'),
        ('ARA', 'Arabic Air'),
    )
    Locations = (
        ('CAI', 'Cairo Airport'),
        ('HGR', ' Hurghada Airport'),
        ('HBE', 'Borg El Arab Airport'),
        ('SSH', 'Sharm El Sheikh Airport'),
    )

    Airline_name = models.CharField(
        max_length=15, choices=Companies, default="Egypt Air")
    From = models.CharField(
        max_length=30, choices=Locations, default="Cairo Airport")
    To = models.CharField(max_length=30, choices=Locations,
                          default="Hurghada Airport")
    Depart = models.DateTimeField()
    Capacity = models.IntegerField(default=30)
    Price = models.FloatField()

    def __str__(self):
        return f"{self.get_Airline_name_display()} flight from {self.get_From_display()} to {self.get_To_display()} depature at {self.Depart} for {self.Price}$"


class Flight_Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Flight_Info = models.ForeignKey(Flights, on_delete=models.CASCADE)
    tickets = models.IntegerField()

    def __str__(self):
        return f"""{self.tickets} tickets for flight {self.Flight_Info.get_Airline_name_display()} 
        from {self.Flight_Info.From} to {self.Flight_Info.To} at {self.Flight_Info.Depart}"""

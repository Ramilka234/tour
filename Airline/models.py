from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Flights(models.Model):
    Companies = (
        ('EGA', 'Egypt Air'),
        ('NIA', 'Pobeda'),
        ('ARA', 'Arabic Air'),
    )
    Locations = (
        ('CAI', 'Moscow Airport'),
        ('HGR', ' Hurghada Airport'),
        ('HBE', 'Borg El Arab Airport'),
        ('SSH', 'Kazan Airport'),
    )

    Airline_name = models.CharField(
        max_length=15, choices=Companies, default="Pobeda")
    From = models.CharField(
        max_length=30, choices=Locations, default="Moscow Airport")
    To = models.CharField(max_length=30, choices=Locations,
                          default="Borg El Arab Airport")
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

class Offer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.offer.title}"
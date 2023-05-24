from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room (models.Model):
    Rtype = (
        ('SIG', 'Single'),
        ('DOB', 'Double'),
        ('DEX', 'Deluxe'),
    )
    Hotels =(
        ('FRS','Four Season'),
        ('HIL','Hilton'),
        ('MAR','Marriot'),
    )
    Hname = models.CharField(max_length=20,choices=Hotels,default="Hilton")
    Rnum = models.IntegerField(unique=True)
    Rcategory = models.CharField(max_length=3, choices=Rtype)
    Descrption = models.CharField(max_length=550)
    Cap = models.IntegerField()
    price = models.IntegerField(default=0)

    def __str__(self):
        return f'Room #{self.Rnum} in {self.Hname} Hotel for {self.Cap} people price is {self.price}$'


class Reserve_Room (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Room = models.ForeignKey(Room, on_delete=models.CASCADE, default='100')
    Rcheck_in = models.DateTimeField()
    Rcheck_out = models.DateTimeField()

    def __str__(self):
        return f' Room #{self.Room.Rnum} in {self.Room.get_Hname_display()} from {self.Rcheck_in} to {self.Rcheck_out}'
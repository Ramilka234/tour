
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')
    vip = models.BooleanField(default=False)
    amount_to_pay = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'




from django.urls import path
from . import views

urlpatterns = [
    path('reserve/<str:rtype>',views.booking, name="booking"),
]


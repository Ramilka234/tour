
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="Home"),
    path('register/',views.Register,name='Register'),
    path('login/',views.Login,name='Login'),
    path('logout/',views.Logout,name='Logout'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('booking-list/<int:ID>',views.booking_list,name='booking_list'),
]
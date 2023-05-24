from django.http import HttpResponse
from django.shortcuts import render
from .forms import FlightForm
from .models import Flights
from UserAccount.models import Profile
# Create your views here.


def flight_booking(request, det_from, det_to, y=0):

    F_form = FlightForm(request.POST)
    F_form.fields['Flight_Info'].queryset = Flights.objects.filter(
        From=det_from, To=det_to).exclude(Capacity=0)

    if request.method == 'POST':

        if F_form.is_valid():

            customer = Profile.objects.get(user_id=request.user.id)
            cFlight = F_form['Flight_Info'].value()
            FTicket = int(F_form['tickets'].value())
            Flight = Flights.objects.get(pk=cFlight)

            if Flight.Capacity <= 0:
                return HttpResponse(f'This flight is full')

            elif FTicket > Flight.Capacity:
                return HttpResponse(f"U selected {FTicket} tickets and this flight has only {Flight.Capacity} tickets remaining")
            elif FTicket <= 0:
                return HttpResponse(f"U selected {FTicket} tickets please enter a vaild number")
            else:
                F_form.instance.user = request.user
                F_form.save()
                if customer.vip:
                  customer.amount_to_pay += (Flight.Price * FTicket) * (1- 0.1)
                  customer.save()
                else:
                   customer.amount_to_pay += Flight.Price * FTicket
                   customer.save()
                Flight.Capacity -= FTicket
                Flight.save()
                return HttpResponse(f'Ur Flight of {Flight} is booked ')

    if(y == 1):
        return F_form
    return render(request, 'index.html', {'Fform': F_form, 'det_from': det_from, 'det_to': det_to})

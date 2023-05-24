from django.shortcuts import redirect, render
from django.http import HttpResponse
from datetime import datetime
from .forms import ReserveForm
from .models import Reserve_Room, Room
from UserAccount.models import Profile
# Create your views here.


def booking(request, rtype, x=0):
    form = ReserveForm(request.POST)

    form.fields['Room'].queryset = Room.objects.filter(Rcategory=rtype)#single

    if request.method == 'POST':

        if form.is_valid():
            form_checkIn = datetime.strptime(
                form['Rcheck_in'].value(), "%Y-%m-%dT%H:%M")

            form_checkOut = datetime.strptime(
                form['Rcheck_out'].value(), "%Y-%m-%dT%H:%M")

            Croom = form['Room'].value()

            customer = Profile.objects.get(user_id=request.user.id)

            money = Room.objects.get(pk=Croom)

            room = Reserve_Room.objects.filter(Room=Croom)

            if form_checkIn < form_checkOut:

                if len(room) <= 0:
                    form.instance.user = request.user
                    form.save()
                    if customer.vip:
                        customer.amount_to_pay += money.price * (1 - 0.1)
                        customer.save()
                    else:
                    
                        customer.amount_to_pay += money.price
                        customer.save()
                    return redirect('Home')

                good = 1

                for book in room:

                    if book.Rcheck_in > form_checkOut or book.Rcheck_out < form_checkIn:
                        pass
                    else:
                        good = 0
                        return HttpResponse("not avalible")
                if good == 1:
                    form.instance.user = request.user
                    form.save()
                    if customer.vip:
                        customer.amount_to_pay += money.price * (1 - 0.1)
                        customer.save()
                    else:
                    
                        customer.amount_to_pay += money.price
                        customer.save()

                    x = 0
                    return HttpResponse("u r booked")

            else:
                print("Enter vaild time period")
    if(x == 1):
        return form
    return render(request, 'index.html', {'form': form, 'rtype': rtype})

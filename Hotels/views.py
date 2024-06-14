from django.shortcuts import redirect, render
from django.http import HttpResponse
from datetime import datetime
from .forms import ReserveForm
from .models import Reserve_Room, Room
from UserAccount.models import Profile
from datetime import timedelta

def booking(request, rtype, x=0):
    form = ReserveForm(request.POST)
    form.fields['Room'].queryset = Room.objects.filter(Rcategory=rtype)

    if request.method == 'POST':
        if form.is_valid():
            form_checkIn = datetime.strptime(form['Rcheck_in'].value(), "%Y-%m-%dT%H:%M")
            form_checkOut = datetime.strptime(form['Rcheck_out'].value(), "%Y-%m-%dT%H:%M")
            Croom = form['Room'].value()
            customer = Profile.objects.get(user_id=request.user.id)
            room_price = Room.objects.get(pk=Croom).price

            if form_checkIn < form_checkOut:
                # Вычисляем количество дней проживания
                days_stayed = (form_checkOut - form_checkIn).days

                # Вычисляем стоимость проживания за каждый день
                total_room_price = room_price * days_stayed

                # Сохраняем бронирование номера
                form.instance.user = request.user
                form.save()

                # Добавляем стоимость проживания за каждый день к общей сумме к оплате
                if customer.vip:
                    customer.amount_to_pay += total_room_price * (1 - 0.1)
                else:
                    customer.amount_to_pay += total_room_price
                customer.save()

                return redirect('Home')

            else:
                print("Enter valid time period")

    if x == 1:
        return form

    return render(request, 'index.html', {'form': form, 'rtype': rtype})
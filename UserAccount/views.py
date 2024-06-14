from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from Hotels.views import booking
from Airline.views import flight_booking
from Hotels.models import Reserve_Room, Room
from Airline.models import Flight_Reserve, Flights, Offer, Booking


# Create your views here.


def index(request):
    rtype = request.GET.get('rtype')
    det_to = request.GET.get('det_to')
    det_from = request.GET.get('det_from')
    prof = "False"
    if request.user.id is not None:
        prof = Profile.objects.get(user_id=request.user)

    if request.method == 'POST':
        offer_id = request.POST.get('offer_id')
        if offer_id:
            offer = get_object_or_404(Offer, id=offer_id)
            Booking.objects.create(user=request.user, offer=offer)
            return redirect('booking_list', ID=request.user.id)

    if 'Hotels' in request.GET:
        if rtype is not None:
            form = booking(request, rtype, 1)
            return redirect('booking', rtype)

    if 'Flights' in request.GET:
        if det_to != 'None':

            if det_from != 'None':
                Fform = flight_booking(request, det_from, det_to, 1)
                return redirect('flight', det_from, det_to)
    offers = Offer.objects.filter(available=True)

    return render(request, 'index.html', {'rtype': rtype, 'det_to': det_to, 'det_from': det_from, 'profile': prof, 'offers': offers})




def Login(request):
    if request.method == 'POST':
        usern = request.POST['username']
        pass1 = request.POST['Password1']

        user = authenticate(request, username=usern, password=pass1)
        if user is not None:
            login(request, user)
            
            return redirect('Home')
        else:
            
            return redirect('Login')

    return render(request, 'login.html')


def Register(request):
    form = ProfileForm(request.POST, request.FILES)
    if request.method == 'POST':

        usern = request.POST['username']
        fname = request.POST['FirstName']
        lname = request.POST['LastName']
        Email = request.POST['EMAIL']
        pass1 = request.POST['Password1']
        pass2 = request.POST['Password2']
        if pass1 == pass2:
            if User.objects.filter(email=Email).exists():
                messages.info(request, 'Email exists')
                return redirect('Register')
            elif User.objects.filter(username=usern).exists():
                messages.info(request, 'Username exists')
                return redirect('Register')
            else:
                Nuser = User.objects.create_user(
                    username=usern, first_name=fname, last_name=lname, email=Email,
                    password=pass1
                )
                Nuser.save()
                if form.is_valid:
                    event = form.save(commit=False)
                    event.user = Nuser
                    event.save()

                return redirect('Login')
        else:
            messages.info(request, 'Passwords dosent match')
            return redirect('Register')

    return render(request, 'Register.html', {'form': form})


def Logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('Login')


def profile(request, username):

    user = User.objects.get(username=username)
    prof = Profile.objects.get(user_id=request.user.id)
    change = 0
    if request.method == 'POST':
        if "UPDATE" in request.POST:
            change = 1
        elif "SAVE" in request.POST:
            user.first_name = request.POST['firstName']
            user.last_name = request.POST['lastName']
            user.email = request.POST['EMAIL']
            user.save()
            return redirect('profile', username)

    return render(request, 'profile.html', {'prof': prof, 'change': change})


def booking_list(request, ID):
    flights = Flight_Reserve.objects.filter(user_id=ID)
    rooms = Reserve_Room.objects.filter(user_id=ID)
    offers = Booking.objects.filter(user_id=ID)
    num_days = 0
    customer = Profile.objects.get(user_id=ID)
    for room in rooms:
        num_days = (room.Rcheck_out - room.Rcheck_in).days
        room.Room.price *= num_days  # Обновление стоимости на основе количества дней
        room.save()
        customer.amount_to_pay = 0
        customer.amount_to_pay -= room.Room.price

    if request.method == 'POST':
        if 'Droom' in request.POST:
            # Fetch the room reservation object to be deleted
            DRoom = Reserve_Room.objects.get(id=request.POST['Droom'])

            # Update the customer's amount to pay based on the room price
            if customer.vip:
                customer.amount_to_pay -= DRoom.Room.price * (1 - 0.1)  # Apply discount for VIP customers
            else:
                customer.amount_to_pay -= DRoom.Room.price

            # Save the updated customer data
            customer.save()

            # Delete the room reservation object
            DRoom.delete()

        if 'Dflight' in request.POST:
            DFlight = Flight_Reserve.objects.get(id=request.POST['Dflight'])
            Flight = Flights.objects.get(id=DFlight.Flight_Info.id)
            if customer.vip:
                customer.amount_to_pay -= (DFlight.Flight_Info.Price + DFlight.tickets) * (1 - 0.1)
                customer.save()
            else:
                customer.amount_to_pay -= DFlight.Flight_Info.Price + DFlight.tickets
                customer.save()
            Flight.Capacity += DFlight.tickets
            Flight.save()
            DFlight.delete()

        if 'Doffer' in request.POST:  # Логика удаления предложения
            DOffer = Booking.objects.get(id=request.POST['Doffer'])
            if customer.vip:
                customer.amount_to_pay -= DOffer.offer.new_price * (1 - 0.1)
            else:
                customer.amount_to_pay -= DOffer.offer.new_price
            customer.save()
            DOffer.delete()

    return render(request, 'Cart.html', {'rooms': rooms, 'flights': flights, 'offers': offers})



# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sessions.backends.db import *
from django.views import View
from decimal import Decimal



def home(request):
    buses = Bus.objects.all()
    return render(request, 'myapp/home.html', {'buses': buses})
def about_us(request):
    return render(request, 'myapp/about.html')

def seat_book(request):
    return render(request, 'myapp/seat_book.html')


import re


def signup(request):
    if request.method == 'POST':
        un = request.POST['username']
        fn = request.POST['fname']
        ln = request.POST['lname']
        en = request.POST['email']
        cn = request.POST['contact_number']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Password validation: minimum length of 8 characters and at least one special character
        if len(pass1) < 8 or not re.search("[!@#$%^&*()_+-=]", pass1):
            messages.error(request, 'Password must be at least 8 characters and contain at least one special character')
            return redirect('signup')

        # Validate phone number: Must contain 10 digits and not all zeros
        if not re.match(r'^[1-9]\d{9}$', cn) or cn == '0000000000':
            messages.error(request, 'Please enter a valid phone number')
            return redirect('signup')

        # Other validations
        if not fn.isalpha():
            messages.error(request, 'First name field must contain alphabets')
            return redirect('signup')
        elif pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        elif User.objects.filter(email=en):
            messages.error(request, 'Email already exists')
            return redirect('signup')
        elif User.objects.filter(username=un):
            messages.error(request, 'Username already exists')
            return redirect('signup')
        else:
            usr = User.objects.create_user(un, en, pass1)
            usr.first_name = fn
            usr.last_name = ln
            usr.save()
            reg = Register_table(user=usr, contact_number=cn)
            reg.save()
            return render(request, 'myapp/signin.html',
                          {"status": "Dear {} your account created successfully".format(fn)})

    return render(request, 'myapp/signup.html')

def signin(request):
    if request.method == 'POST':
        un = request.POST['username']
        pwd = request.POST['pass1']
        user = authenticate(username=un, password=pwd)
        if user:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                return HttpResponseRedirect("/findbus")
        else:
            messages.error(request, 'Username or password incorrect')
            return render(request, 'myapp/signin.html')
    return render(request, 'myapp/signin.html')

def signout(request):
    logout(request)
    return redirect('/')

def user_home(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/user_home.html', context)

def profile(request):
    if request.method == 'POST':
        name = request.POST['name']
        addr1 = request.POST['addr1']
        addr2 = request.POST['addr2']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        data = Profile(name=name, addr1=addr1, addr2=addr2, city=city, state=state, zipcode=zipcode)
        data.save()
        res = "Dear {} Your Profile is saved succesfully".format(name)
        return render(request, 'myapp/profile.html', {'status': res})
    return render(request, 'myapp/profile.html')



def view_profile(request):
    data = Register_table.objects.get(user__id=request.user.id)

    return render(request, 'myapp/view_profile.html', {'data': data})

def edit_profile(request):
    data = Register_table.objects.get(user__id=request.user.id)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        en = request.POST['email']
        cn = request.POST['contact_number']
        age = request.POST['age']
        cty = request.POST['city']
        occ = request.POST['occ']
        abt = request.POST['about']
        gen = request.POST['gender']

        # validate first and last name fields
        if not re.match("^[A-Za-z]+$", fn) or not re.match("^[A-Za-z]+$", ln):
            messages.error(request, 'Name should contain only alphabets')
            return render(request, 'myapp/edit_profile.html', {'data': data})

        # validate age field
        if not age.isdigit() or int(age) <= 0 or age == '00':
            messages.error(request, 'Age should be a positive number and greater than 00')
            return render(request, 'myapp/edit_profile.html', {'data': data})

        # validate phone number field
        if not re.match("^[0-9]{10}$", cn) or cn == '0000000000':
            messages.error(request, 'Phone number should be a 10-digit number and not 0000000000')
            return render(request, 'myapp/edit_profile.html', {'data': data})

        # validate occupation and about fields
        if not re.match("^[A-Za-z ]+$", occ) or not re.match("^[A-Za-z ]+$", abt):
            messages.error(request, 'Occupation and About fields should contain only alphabets')
            return render(request, 'myapp/edit_profile.html', {'data': data})

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = en
        usr.save()

        data.contact_number = cn
        data.age = age
        data.city = cty
        data.occupation = occ
        data.about = abt
        data.gender = gen
        data.save()

        if 'profile_img' in request.FILES:
            img = request.FILES['profile_img']
            data.profile_pic = img
            data.save()
        messages.success(request, 'Updated Successfully...!!!')
    return render(request, 'myapp/edit_profile.html', {'data': data})

class change_password(View):

    def get(self, request):
        return render(request, 'myapp/change_password.html')

    def post(self, request):
        current_pas = request.POST['ppwd']
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username
        pwd = new_pas
        check = user.check_password(current_pas)
        if check == True:
            user.set_password(new_pas)
            user.save()
            msz = "Password changed successfully"
            col = "alert-success"
            user = User.objects.get(username=un)
            login(request, user)
            return render(request, 'myapp/change_password.html', {'msz': msz, 'col': col})
        else:
            msz = "Incorrect Previous Password"
            col = "alert-danger"
            return render(request, 'myapp/change_password.html', {'msz': msz, 'col': col})


def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source').lower()
        dest_r = request.POST.get('destination').lower()
        date_r = request.POST.get('date')
        date_r = datetime.strptime(date_r, "%Y-%m-%d").date()
        bus_list = Bus.objects.filter(busroute__source__iexact=source_r, busroute__dest__iexact=dest_r, date=date_r)
        if bus_list:
            return render(request, 'myapp/list.html', {'bus_list': bus_list})
        else:
            context['data'] = request.POST
            context["error"] = "No available Bus Schedule for entered Route and Date"
            return render(request, 'myapp/findbus.html', context)
    else:
        return render(request, 'myapp/findbus.html')

from django.contrib.auth.decorators import login_required

@login_required
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.filter(id=id_r).first()
        if bus:
            if bus.rem >= seats_r:
                name_r = bus.bus_name
                cost = seats_r * bus.busroute_set.first().price
                route = bus.busroute_set.first()
                source_r = route.source
                dest_r = route.dest
                nos_r = Decimal(bus.nos)
                price_r = route.price
                date_r = bus.date
                time_r = bus.time
                email_r = request.user.email
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(
                    bus=bus,
                    email=email_r,
                    name=name_r,
                    price=cost,
                    date=date_r,
                    time=time_r,
                    status='BOOKED',
                    nos=seats_r  # add the number of seats booked to the Book object
                )

                # Handling passenger details
                passenger_names = request.POST.getlist('passenger_name[]')
                passenger_ages = request.POST.getlist('passenger_age[]')
                passenger_genders = request.POST.getlist('passenger_gender[]')

                for i in range(len(passenger_names)):
                    passenger = Passenger.objects.create(
                        book=book,
                        name=passenger_names[i],
                        age=int(passenger_ages[i]),
                        gender=passenger_genders[i]
                    )

                return render(request, 'myapp/bus_payment.html', locals())
            else:
                context["error"] = "Sorry, there are not enough seats available."
                return render(request, 'myapp/findbus.html', context)
        else:
            context["error"] = "Bus not found."
            return render(request, 'myapp/findbus.html', context)
    else:
        return render(request, 'myapp/findbus.html')

from django.db import transaction


def cancellings(request):
    context = {}
    if request.method == 'POST':
        book_id = request.POST.get('booking_id')

        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(id=book_id)
                bus = book.bus
                print("Before update - Remaining seats:", bus.rem)
                rem_r = bus.rem + book.nos
                bus.rem = rem_r
                bus.save(update_fields=['rem'])
                book.status = 'CANCELLED'
                book.nos = 0
                book.save(update_fields=['status', 'nos'])
                print("After update - Remaining seats:", bus.rem)

            messages.success(request, "Booked bus has been cancelled successfully.")
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry, you have not booked that bus."
            return render(request, 'myapp/error.html', context)
    else:
        book_list = Book.objects.filter(user=request.user)
        context['book_list'] = book_list
        return render(request, 'myapp/findbus.html', context)

def seebookings(request):
    context = {}
    email = request.user.email
    book_list = Book.objects.filter(email=email).select_related('bus')

    for book in book_list:
        passenger_count = Passenger.objects.filter(book=book).count()
        book.total_seats = passenger_count

    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry, no buses booked."
        return render(request, 'myapp/findbus.html', context)


def check_user(request):
    if request.method == "GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


def convert_expiry_date(expiry_date_str):
    expiry_date_parts = expiry_date_str.split('/')
    expiry_month = int(expiry_date_parts[0])
    expiry_year = int(expiry_date_parts[1])
    # Assuming that the expiry day is the last day of the month
    last_day_of_month = 28 + (expiry_month + int(expiry_month / 8)) % 2 + 2 % expiry_month + 2 * int(1 / expiry_month)
    expiry_date = datetime(expiry_year, expiry_month, last_day_of_month)
    return expiry_date.strftime('%Y-%m-%d')

def bus_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        card_holder_name = request.POST.get('card_holder_name')
        card_number = request.POST.get('card_number')
        cvv = request.POST.get('cvv')
        expiry_date_str = request.POST.get('expiry_date')
        expiry_date = convert_expiry_date(expiry_date_str)

        suc = Payment(amount=amount,
                      card_number=card_number, cvv=cvv, expiry_date=expiry_date,card_holder_name=card_holder_name )
        suc.save()
        context = {'msg': 'payment successful'}
        return render(request, './myapp/bookings.html', context)
    else:
        context = {}  # Define an empty context dictionary or pass your own context
        return render(request, './myapp/bus_payment.html', context)





# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal


# Create your models here.
def validate_remaining_seats(nos, rem):
    if rem is None or nos is None:
        raise ValidationError('Number of seats, remaining seats and price cannot be None')
    elif rem > nos:
        raise ValidationError('Remaining seats cannot be greater than total seats')
    elif nos == 0:
        raise ValidationError('Number of seats cannot be zero')
    elif rem == 0:
        raise ValidationError('Remaining seats cannot be zero')
    elif rem < 0:
        raise ValidationError('Remaining seats cannot be negative')
    elif nos < 1:
        raise ValidationError('Number of seats should be at least 1')






def validate_price_not_zero(value):
    if value == 0:
        raise ValidationError('Price cannot be zero.')


class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    bus_number = models.CharField(max_length=6, unique=True)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(upload_to='images')

    class Meta:
        verbose_name_plural = "List of Buses"

    def __str__(self):
        return self.bus_number

    def clean(self):
        # Check if bus number is longer than 6 characters
        if len(self.bus_number) > 6:
            raise ValidationError("Bus number should contain a maximum of 6 characters.")

        # Check if bus number contains at least 4 digits
        digit_count = sum(1 for char in self.bus_number if char.isdigit())
        if digit_count < 4:
            raise ValidationError("Bus number should contain at least 4 digits.")

        # Check if another bus with the same bus number exists
        if Bus.objects.exclude(pk=self.pk).filter(bus_number=self.bus_number).exists():
            raise ValidationError("Bus number already exists.")

        # Add any other validation logic here
        validate_remaining_seats(self.nos, self.rem)


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'), (CANCELLED, 'Cancelled'),)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)
    nos = models.IntegerField(default=0)  # Add the nos field to represent the number of seats

    class Meta:
        verbose_name_plural = "List of Books"

    def __str__(self):
        return self.email



class Passenger(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    def clean(self):
        if self.age < 0:
            raise ValidationError('Age cannot be negative.')

    def __str__(self):
        return str(self.name)

class BusRoute(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2, max_digits=6, validators=[validate_price_not_zero])

    class Meta:
        verbose_name_plural = "Bus Routes"



class Register_table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True,default='profile_pic/default.png')
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True, default="Male")
    occupation = models.CharField(max_length=200, null=True, blank=True)
    added_on = models.DateField(auto_now_add=True, null=True, blank=True)
    uploaded_on = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class Profile(models.Model):
    state_choices = [
        ('Kerala','Kerala'),
        ('Gujrat','Gujrat'),
        ('Mumbai','Mumbai'),
        ('Karnataka','Karnataka'),
    ]
    name = models.CharField(max_length=50)
    addr1 = models.CharField(max_length=400)
    addr2 = models.CharField(max_length=400)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50,choices=state_choices)
    zipcode = models.IntegerField()




class Payment(models.Model):
    amount = models.FloatField()
    card_holder_name = models.CharField(max_length=50)
    card_number = models.IntegerField()
    cvv = models.IntegerField()
    expiry_date = models.DateField()


    def __str__(self):
        return self.card_holder_name



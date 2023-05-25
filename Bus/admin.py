from django.contrib import admin
from .models import Bus, Register_table, Book,Payment,BusRoute,Passenger
# Register your models here.

admin.site.register(Bus)
admin.site.register(Register_table)
admin.site.register(Book)
admin.site.register(Payment)
admin.site.register(BusRoute)
admin.site.register(Passenger)



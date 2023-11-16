from django.contrib import admin
from  personal.models import User, Lieu, Reservation
# Register your models here.
admin.site.register(User)
admin.site.register(Lieu)
admin.site.register(Reservation)
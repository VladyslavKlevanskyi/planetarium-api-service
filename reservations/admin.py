from django.contrib import admin
from reservations.models import Reservation, Ticket, ShowSession

admin.site.register(ShowSession)
admin.site.register(Reservation)
admin.site.register(Ticket)

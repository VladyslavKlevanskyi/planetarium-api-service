from django.contrib import admin
from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    Reservation,
    ShowSession,
    Ticket,
)

admin.site.register(ShowTheme)
admin.site.register(AstronomyShow)
admin.site.register(Reservation)
admin.site.register(ShowSession)
admin.site.register(Ticket)

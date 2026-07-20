from django.contrib import admin
from .models import Play, Ticket, Reservation, Genre, Performance, TheatreHall, Actor


admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Play)
admin.site.register(TheatreHall)
admin.site.register(Performance)
admin.site.register(Reservation)
admin.site.register(Ticket)
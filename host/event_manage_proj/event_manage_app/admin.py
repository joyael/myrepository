from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(EventCategory)
admin.site.register(Ticket)
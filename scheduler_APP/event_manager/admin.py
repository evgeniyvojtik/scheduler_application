from django.contrib import admin

# Register your models here.
from event_manager.models import MyUser, Event, CountryHoliday

admin.site.register(MyUser)
admin.site.register(Event)
admin.site.register(CountryHoliday)
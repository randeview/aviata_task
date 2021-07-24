from django.contrib import admin

from apps.core.models import City, Directories, Flight


class FlightAdmin(admin.ModelAdmin):
    list_display = ['from_city', 'to_city', 'flight_date', 'price', 'duration', 'flight_checked']


admin.site.register(City)
admin.site.register(Directories)
admin.site.register(Flight, FlightAdmin)

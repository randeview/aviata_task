import requests
from datetime import datetime, timedelta

from apps.core.models import Directories, Flight
from apps.core.services import RedisClient, SkyPicker
from config.celery_app import app


@app.task
def get_flights():
    date_from = datetime.today().strftime('%d/%m/%Y')
    date_to = (datetime.today() + timedelta(weeks=4)).strftime('%d/%m/%Y')

    sky_picker = SkyPicker(method='flights')

    for directory in Directories.objects.all():
        data = sky_picker.get_flights(fly_from=directory.from_city.code, fly_to=directory.to_city.code,
                                      date_from=date_from,
                                      date_to=date_to)
        Flight.create_update_flights(data, fly_from=directory.from_city, fly_to=directory.to_city)


@app.task
def check_flight():
    sky_picker = SkyPicker(method='check_flights')
    queryset = Flight.objects.not_checked()
    for flight in queryset:
        data = sky_picker.check_flight(flight.booking_token)
        flight.flight_invalid = data.get("flights_invalid", False)
        flight.flight_checked = data.get("flights_checked", False)
        if data.get("price_change"):
            flight.price = data.get("flights_price")
        flight.save(update_fields=['flight_invalid', 'flight_checked', 'price'])
import requests
from datetime import datetime, timedelta

from apps.core.models import Directories, Flight
from apps.core.services import RedisClient, SkyPicker
from config.celery_app import app


def create_update_flights(flight_data, fly_from, fly_to):
    objects_pool_create = []
    flight = {
        'from_city': fly_from,
        'to_city': fly_to
    }
    for choice in flight_data:
        flight['price'] = choice['price']
        flight['flight_date'] = datetime.fromtimestamp(choice['dTimeUTC']).date()
        flight['airlines'] = ', '.join(choice['airlines']),
        flight['duration'] = choice['fly_duration'],
        flight['flight_id'] = choice['id']
        flight['booking_token'] = choice['booking_token']
        if Flight.objects.filter(flight_id=choice['id']).exists():
            Flight.objects.filter(flight_id=choice['id']).update(**flight)
            continue
        objects_pool_create.append(Flight(**flight))
    Flight.objects.bulk_create(objects_pool_create)
    return len(objects_pool_create)


@app.task
def get_flights():
    date_from = datetime.today().strftime('%d/%m/%Y')
    date_to = (datetime.today() + timedelta(weeks=4)).strftime('%d/%m/%Y')

    sky_picker = SkyPicker(method='flights')

    for directory in Directories.objects.all():
        data = sky_picker.get_flights(fly_from=directory.from_city.code, fly_to=directory.to_city.code,
                                      date_from=date_from,
                                      date_to=date_to)
        create_update_flights(data.get('data'),
                              fly_from=directory.from_city,
                              fly_to=directory.to_city)

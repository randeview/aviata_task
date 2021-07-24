import os.path
from datetime import datetime, timedelta

from django.conf import settings
import redis
import requests


class RedisClient:
    def __init__(self, host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def send(self, key, value):
        self.redis.publish(key, value)


class SkyPicker:
    base_url = settings.SKY_PICKER_URL
    check_url = settings.SKY_CHECK_URL
    partner = settings.PARTNER_AFFIL_ID
    headers = {'Content-Type': 'application/json'}
    count_flights = 3

    def __init__(self, method, *args, **kwargs):
        self.method = method
        self.url = os.path.join(self.base_url, method)

    def get_most_cheap_flights(self, response):
        data = response.get('data', [])
        return sorted(data, key=lambda k: k['price'])[:self.count_flights]

    def get_flights(self, fly_from, fly_to, date_from, date_to):
        params = {
            'fly_from': fly_from,
            'fly_to': fly_to,
            'partner': self.partner,
            'date_from': date_from,
            'date_to': date_to,
            'adults': 1,
            'infants': 1
        }

        response = requests.get(self.url, params=params, headers=self.headers)
        if response.ok:
            return self.get_most_cheap_flights(response.json())
        else:
            return self.handle_service_exception(response)

    def check_flight(self, booking_token, pnum=1, bnum=1, adults=1):
        self.url = os.path.join(self.check_url, self.method)
        params = {
            'booking_token': booking_token,
            'pnum': pnum,
            'bnum': bnum,
            'adults': adults,
        }
        response = requests.get(self.url, params=params, headers=self.headers)
        if response.ok:
            return response.json()
        else:
            return self.handle_service_exception(response)

    def handle_service_exception(self, response):
        return response.text

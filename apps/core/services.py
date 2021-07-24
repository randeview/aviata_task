import os.path
from datetime import datetime, timedelta

from django.conf import settings
import redis
import requests


class RedisClient:
    def __init__(self, host=settings.REDIS_HOST,
                 port=settings.REDIS_PORT, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)

    def send(self, key, value):
        self.redis.publish(key, value)


class SkyPicker:
    base_url = settings.SKY_PICKER_URL
    partner = settings.PARTNER_AFFIL_ID

    def __init__(self, method, *args, **kwargs):
        self.method = method
        self.url = os.path.join(self.base_url, method)

    def get_flights(self, fly_from, fly_to, date_from, date_to):
        params = {
            'fly_from': fly_from,
            'fly_to': fly_to,
            'partner': self.partner,
            'date_from': date_from,
            'date_to': date_to,
        }

        response = requests.get(self.url, params=params)
        if response.ok:
            return response.json()
        else:
            return self.handle_service_exception(response)

    def handle_service_exception(self, response):
        return response.text

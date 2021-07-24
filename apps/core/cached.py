from datetime import datetime

from apps.core.services import RedisClient

redis_client = RedisClient()


def create_update_flights_cache(flight_data, fly_from, fly_to):
    redis_client.redis.flushdb()
    flight_result = []
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
        flight_result.append(flight)
    redis_client.redis.set(f'{fly_from}-{fly_to}', str(flight_result))


def get_cached_data():
    keys = redis_client.redis.keys('*')
    flights = []
    for k in keys:
        flights.append(redis_client.redis.get(k).decode('UTF-8'))
    return flights

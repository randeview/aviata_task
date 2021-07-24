from datetime import datetime

from django.db import models

from apps.core.managers import FlightsQueryset


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        "Время создания", auto_now_add=True, db_index=True
    )
    changed_at = models.DateTimeField(
        "Время последнего изменения", auto_now=True, db_index=True
    )

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField('Названия', max_length=255)
    code = models.CharField('Код', max_length=4)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Directories(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='directories_from')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='directories_to')

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f"{self.from_city.name} -> {self.to_city.name}"


class Flight(TimestampMixin):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='flights_from')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='flights_to')
    flight_id = models.TextField('Идентификатор полета')
    booking_token = models.TextField('Токен брони')
    price = models.DecimalField('Цена', max_digits=16, decimal_places=2)
    flight_date = models.DateField('Дата вылета')
    airlines = models.CharField('Авиакомпании', max_length=100)  # Add fk model for airline
    duration = models.CharField('Длительность полета', max_length=50)
    flight_checked = models.BooleanField('Проверен ли билет', default=False)
    flight_invalid = models.BooleanField('Полет не валидный', default=False)

    objects = FlightsQueryset.as_manager()

    class Meta:
        verbose_name = 'Полет'
        verbose_name_plural = 'Полеты'

    def __str__(self):
        return f"{self.from_city.name} -> {self.to_city.name}"

    @classmethod
    def create_update_flights(cls, flight_data, fly_from, fly_to):
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
            if cls.objects.filter(flight_id=choice['id']).exists():
                cls.objects.filter(flight_id=choice['id']).update(**flight)
                continue
            objects_pool_create.append(Flight(**flight))
        cls.objects.bulk_create(objects_pool_create)
        return len(objects_pool_create)

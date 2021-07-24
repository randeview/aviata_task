from django.db import models


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

    class Meta:
        verbose_name = 'Полет'
        verbose_name_plural = 'Полеты'

    def __str__(self):
        return f"{self.from_city.name} -> {self.to_city.name}"

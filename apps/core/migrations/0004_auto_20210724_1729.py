# Generated by Django 3.2.5 on 2021-07-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_flight'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='flight_checked',
            field=models.BooleanField(default=False, verbose_name='Проверен ли полет'),
        ),
        migrations.AddField(
            model_name='flight',
            name='flight_invalid',
            field=models.BooleanField(default=False, verbose_name='Полет не валидный'),
        ),
    ]

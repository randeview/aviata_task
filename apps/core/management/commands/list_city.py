import json
import os

from django.core.management.base import BaseCommand
from apps.core.models import City


class Command(BaseCommand):
    help = 'List name,code of city'

    def handle(self, *args, **options):
        configuration_file = 'cities.json'
        if not os.path.isfile(configuration_file):
            print('NO file')
        f = open(configuration_file, "r")
        data = json.loads(f.read())
        for i in data:
            pk = i['pk']

            if not City.objects.filter(id=pk).exists():
                City.objects.create(id=pk, **i['fields'])
            else:
                service = City.objects.get(id=pk)
                if not any([getattr(service, key_name) for key_name in i['fields'].keys()]):
                    City.objects.filter(id=pk).update(**i['fields'])

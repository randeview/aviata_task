from django.core.management.base import BaseCommand
import os, json

from apps.core.models import City, Directories


class Command(BaseCommand):
    help = 'List directories of city'

    def handle(self, *args, **options):
        configuration_file = 'routes.json'
        if not os.path.isfile(configuration_file):
            print('NO file')
        f = open(configuration_file, "r")
        data = json.loads(f.read())
        for i in data:
            pk = i['pk']

            if not Directories.objects.filter(id=pk).exists():
                from_city = City.objects.get(code=i['fields']['from_city'])
                to_city = City.objects.get(code=i['fields']['to_city'])
                Directories.objects.create(id=pk, from_city=from_city, to_city=to_city)
            else:
                service = Directories.objects.get(id=pk)
                if not any([getattr(service, key_name) for key_name in i['fields'].keys()]):
                    from_city = City.objects.get(code=i['fields']['from_city'])
                    to_city = City.objects.get(code=i['fields']['to_city'])
                    Directories.objects.filter(id=pk).update(from_city=from_city, to_city=to_city)

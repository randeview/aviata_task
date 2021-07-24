from django.core.management.base import BaseCommand
import os, json

from apps.core.models import City, Directories
from apps.core.tasks import get_flights


class Command(BaseCommand):
    help = 'List directories of city'

    def handle(self, *args, **options):
        get_flights()


















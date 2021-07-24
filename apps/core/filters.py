import django_filters

from apps.core import Cities
from apps.core.models import City, Flight


class FLightListFilter(django_filters.FilterSet):
    class Meta:
        model = Flight
        fields = {
            'from_city__name': ['startswith'],
            'to_city__name': ['startswith']
        }
        together = ['from_city__name', 'to_city__name']

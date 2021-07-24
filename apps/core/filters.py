import django_filters

from apps.core.models import City, Flight


class FLightListFilter(django_filters.FilterSet):
    city_from = django_filters.ChoiceFilter(choices=City.objects.values_list('name', flat=True))

    class Meta:
        model = Flight
        fields = [
            'city_from',
        ]

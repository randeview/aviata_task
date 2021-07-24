from rest_framework import views
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.core.filters import FLightListFilter
from apps.core.models import Flight
from apps.core.serializers import FlightSerializer, FlightDetailSerializer


class FlightViewSet(ReadOnlyModelViewSet):
    queryset = Flight.objects.actual().order_by('price')
    serializer_class = FlightSerializer
    retrieve_serializer_class = FlightDetailSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.retrieve_serializer_class

        return self.serializer_class

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = FLightListFilter
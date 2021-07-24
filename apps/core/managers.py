from django.db.models import QuerySet
from datetime import datetime


class FlightsQueryset(QuerySet):
    def actual(self):
        return self.filter(flight_date__gte=datetime.today(), flight_invalid=False)

    def not_checked(self):
        return self.filter(flight_date__gte=datetime.today(), flight_checked=False).exclude(flight_invalid=True)

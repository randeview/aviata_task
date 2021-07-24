from rest_framework import serializers

from apps.core.models import Flight, City


class CitySerialiazer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'code']


class FlightSerializer(serializers.ModelSerializer):
    from_city = serializers.SerializerMethodField()
    to_city = serializers.SerializerMethodField()

    def get_from_city(self, obj):
        return obj.from_city.name

    def get_to_city(self, obj):
        return obj.to_city.name

    class Meta:
        model = Flight
        fields = ['id', 'from_city', 'to_city', 'price', 'flight_date']


class FlightDetailSerializer(serializers.ModelSerializer):
    from_city = CitySerialiazer()
    to_city = CitySerialiazer()

    class Meta:
        model = Flight
        fields = '__all__'

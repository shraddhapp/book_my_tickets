from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class MovieTheatreShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieTheatreShow
        fields = '__all__'


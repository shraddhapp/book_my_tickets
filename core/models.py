from django.db import models
from django.utils.datetime_safe import datetime
# Create your models here.

class City(models.Model):
    city_name = models.CharField(max_length=20, primary_key=True)

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    cust_name = models.CharField(max_length=50)
    pwd = models.CharField(max_length=10)
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)

class Show(models.Model):
    show_name = models.CharField(max_length=20, primary_key=True)
    start_time = models.DateTimeField(default=datetime.now, blank=False)
    end_time = models.DateTimeField(default=datetime.now, blank=False)
    total_seats = models.IntegerField(default=20)
    available_seats = models.IntegerField(default=20)


class Theatre(models.Model):
    theater_name = models.CharField(max_length=20, primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Movie(models.Model):
    movie_name = models.CharField(max_length=20, primary_key=True)

class MovieTheatreShow(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
from django.contrib.auth.models import User

from django.db import models
# Create your models here.


class Subscribe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    email = models.EmailField()
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class WeatherForecastData(models.Model):
    datetime = models.DateTimeField()
    temperature = models.CharField(max_length=100)
    wind_speed = models.CharField(max_length=100)
    humidity = models.CharField(max_length=100)
    precipitation = models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)

    def __str__(self):
        return str(self.datetime)

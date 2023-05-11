from django.contrib import admin
from .models import Subscribe, WeatherForecastData

# Register your models here.
admin.site.register(Subscribe)
admin.site.register(WeatherForecastData)
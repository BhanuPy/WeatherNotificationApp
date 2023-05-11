from django.urls import path
from weather.views import CurrentWeatherView, SubscribeView

urlpatterns = [
    path('', CurrentWeatherView.as_view(), name='current_weather'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]

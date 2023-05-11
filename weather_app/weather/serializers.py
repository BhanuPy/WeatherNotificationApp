from .models import Subscribe, WeatherForecastData
from django.contrib.auth.models import User
from rest_framework import serializers





class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Subscribe
        fields = ['email', 'location']

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        print(user_data)
        print(validated_data)
        if validated_data:
            user = User.objects.create(username=validated_data["email"], email=validated_data["email"])
            subscription = Subscribe.objects.create(user=user, email = validated_data["email"],location = validated_data["location"])
            return subscription

from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework import generics, permissions
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from .models import WeatherForecastData, Subscribe
from .serializers import SubscriptionSerializer
from .utils import get_location, send_subscription_confirmation_email

# class CurrentWeatherView(APIView):
#     def get(self, request):
#         # Get weather data from OpenWeatherMap API
#         city_name = 'New York'
#         url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric'
#         response = requests.get(url)
#         if response.status_code != 200:
#             return Response({'error': 'Failed to fetch weather data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         data = response.json()

#         # Save weather data to the database
#         weather_data = WeatherForecastData.objects.create(
#             temperature=data['main']['temp'],
#             wind_speed=data['wind']['speed'],
#             humidity=data['main']['humidity'],
#             city=data['name'],
#             country=data['sys']['country'],
#             datetime=datetime.now()
#         )

#         # Serialize and return the weather data
#         return Response({
#             'temperature': weather_data.temperature,
#             'wind_speed': weather_data.wind_speed,
#             'humidity': weather_data.humidity,
#             'city': weather_data.city,
#             'country': weather_data.country,
#             'timestamp': weather_data.datetime,
#         })



class CurrentWeatherView(APIView):
    def get(self, request):
        location = get_location()
        city = location["city"]
        country = location["country"]
        try:

            weather_data = get_weather_data(city, country)

            # create_weather_data = WeatherForecastData.objects.create(temperature=temperature,
            #                                                       wind_speed=wind_speed,
            #                                                       humidity=humidity,
            #                                                       precipitation=precipitation,
            #                                                       city=citydata,
            #                                                       country=country,
            #                                                       datetime=datetime.now())
      
            
            # Serialize and return the weather data
            return Response({
                'temperature': weather_data["temperature"],
                'wind_speed': weather_data["wind_speed"],
                'humidity': weather_data["humidity"],
                'precipitation': weather_data["precipitation"],
                'city': weather_data["city"],
                'country': weather_data["country"],
                'timestamp': weather_data["time"],
                })

        except requests.exceptions.HTTPError as err:
            print(f"An HTTP error occurred: {err}")
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")        
 
      
        return Response(None)     

class SubscribeView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, request):
        # print(request.data)
        data=dict()
        data = request.data
        location = get_location()
        data["location"] = str(location["city"]+","+ location["country"])
        print(data)
        # return Response(None)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            subscriber=serializer.save()
            send_subscription_confirmation_email(subscriber.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SubscriptionList(generics.ListCreateAPIView):
#     serializer_class = SubscriptionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Subscribe.objects.filter(user=self.request.user)


# class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Subscribe.objects.all()
#     serializer_class = SubscriptionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         obj = get_object_or_404(Subscribe, pk=self.kwargs['pk'])
#         if obj.user != self.request.user:
#             raise PermissionDenied
#         return obj


def get_weather_data(city_data, country):
    # city_data ="lucknow"
    search_url = f"https://www.google.com/search?q=weather+{city_data}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }
       
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    weather_data = dict()    
    weather_web_data= soup.find("div", {"id": "search"})
    weather_data["humidity"] = weather_web_data.find("span", {"id": "wob_hm"}).text
    weather_data["precipitation"] = weather_web_data.find("span", {"id": "wob_pp"}).text 
    weather_data["wind_speed"] = weather_web_data.find("span", {"id": "wob_ws"}).text
    weather_data["temperature"] = weather_web_data.find('span', class_='wob_t').text+"°C"
    weather_data["country"] = country
    weather_data["city"] = city_data
    weather_data["time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
   

    # forecast_card = soup.find('div', class_='wob_dfc')
    # # print(forecast_card)    
    # for card in forecast_card:
    #     day = card.find('div', class_='Z1VzSb').text
    #     img_alt = card.find('img')['alt']
    #     temperature = card.find('div', class_='gNCp2e').text.replace('°', '')

    #     print(f"Day: {day}")
    #     print(f"Image Alt: {img_alt}")
    #     print(f"Temperature: {temperature}")
    #     print()

    # forecast_card = soup.find('div', class_='wob_dfc')
        
    # if forecast_card:
        # forecast_items = forecast_card.find_all('div', class_='wob_d')
        # print(f"Weather forecast for {city_data} in the next 24 hours:")
        # print(forecast_items)
        # for item in forecast_card:
            # time = item.find('div', class_='wob_t').text
            # temperature = item.find('span', class_='wob_t').text
            # humidity = item.find('div', class_='wob_hm').text
            # wind_speed = item.find('div', class_='wob_ws').text
            #precipitation = item.find('div', class_='wob_pp').text
            
            # print(f"\nTime: {time}")
            # print(f"Temperature: {temperature}°C")
            # print(f"Humidity: {humidity}%")
            # print(f"Wind Speed: {wind_speed}")
            # print(f"Precipitation: {precipitation}")        
   
    
    # else:
        # print(f"Could not find weather forecast for {city_data}")

    # print(weather_web_data)

    # get_hourly_forecast(city_data)    
    return weather_data



# def get_location():
#     res = requests.get('https://ipinfo.io/')
#     # Receiving the response in JSON format
#     data = res.json()
#     # Extracting the Location of the City from the response
#     #print(data)
#     location=dict()
#     location["city"] = data['city']
#     location["country"] = data['country']
#     return location

# def get_hourly_forecast(city):
#     url = f"https://www.timeanddate.com/weather/india/{city}/hourly"
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         print("Hourly Weather Forecast for Lucknow:")
#         print("{:<10} {:<15} {:<10}".format("Time", "Temperature", "Conditions"))
#         weather_data = []
#         table_rows = soup.find_all('tr')
#         for row in table_rows:
#             columns = row.find_all('td')
#             if columns and len(weather_data)<24:
#                 data = dict()
#                 # print(columns)
#                 print()
#                 data["time"] = row.find('th').text.strip()
#                 data["temperature"] = columns[3].text.split()[0]+"°C"
#                 data["weather_report"] = columns[2].text
#                 data["windspeed"] = columns[4].text.strip()
#                 data["humidity"] = columns[6].text
#                 data["precipitation"] = columns[7].text
#                 print(data)
#                 print()
#                 weather_data.append(data)
#         return weather_data        
#         print(len(weather_data))          
#     except requests.exceptions.HTTPError as err:
#         print(f"An HTTP error occurred: {err}")
#     except requests.exceptions.RequestException as err:
#         print(f"An error occurred: {err}")
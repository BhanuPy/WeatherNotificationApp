from django.template.loader import render_to_string
from django.core.mail import send_mail
from bs4 import BeautifulSoup
import requests
from .models import Subscribe
import logging
from django.conf import settings



logger = logging.getLogger(__name__)

def send_message():
    logger.info("Cron job was called")
    subscribers = Subscribe.objects.all()

    # Send email notifications to subscribed users
    for subscriber in subscribers:
        city = subscriber.location.split(",")[0]
        subscriber_weather_data = get_hourly_forecast(city)
        send_weather_forecast_email(subscriber.email, subscriber_weather_data)



def send_subscription_confirmation_email(user_email):
    email_backend = settings.EMAIL_BACKEND
    email_host = settings.EMAIL_HOST
    email_port = settings.EMAIL_PORT
    email_host_user = settings.EMAIL_HOST_USER
    email_host_password = settings.EMAIL_HOST_PASSWORD
    email_use_tls = settings.EMAIL_USE_TLS
    email_use_ssl = settings.EMAIL_USE_SSL
    subject = 'Subscription Confirmation'
    template_name = 'subscription_confirmation_email.html'
    context = {'user': user_email}

    # Render the HTML email template
    html_message = render_to_string(template_name, context)

    # Send the email
    send_mail(
        subject=subject,
        message='Subscription Confirmation',
        from_email=email_host_user,
        recipient_list=[user_email],
        auth_user=email_host_user,
        auth_password=email_host_password,
        html_message=html_message,
    )

    


def send_weather_forecast_email(user_email, weather_data):
    subject = 'Weather Forecast for the Next 24 Hours'
    template_name = 'weather_forecast_email.html'
    context = {'weather_data': weather_data}

    # Render the HTML email template
    html_message = render_to_string(template_name, context)

    # Send the email
    send_mail(
        subject=subject,
        message='Weather Report',
        from_email='weather_data@api.com',
        recipient_list=[user_email],
        html_message=html_message,
    )


def get_location():
    res = requests.get('https://ipinfo.io/')
    # Receiving the response in JSON format
    data = res.json()
    # Extracting the Location of the City from the response
    #print(data)
    location=dict()
    location["city"] = data['city']
    location["country"] = data['country']
    return location


def get_hourly_forecast(city):
    url = f"https://www.timeanddate.com/weather/india/{city}/hourly"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        print("Hourly Weather Forecast for Lucknow:")
        print("{:<10} {:<15} {:<10}".format("Time", "Temperature", "Conditions"))
        weather_data = []
        table_rows = soup.find_all('tr')
        for row in table_rows:
            columns = row.find_all('td')
            if columns and len(weather_data)<24:
                data = dict()
                # print(columns)
                print()
                data["time"] = row.find('th').text.strip()
                data["temperature"] = columns[3].text.split()[0]+"°C"
                data["weather_report"] = columns[2].text
                data["windspeed"] = columns[4].text.strip()
                data["humidity"] = columns[6].text
                data["precipitation"] = columns[7].text
                print(data)
                print()
                weather_data.append(data)
        return weather_data        
        # print(len(weather_data))          
    except requests.exceptions.HTTPError as err:
        print(f"An HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
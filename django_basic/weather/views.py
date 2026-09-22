import requests
from django.shortcuts import render
from .models import WeatherData


def weather(request):

    city = request.GET.get('city')

    if not city:
        return render(request, 'weather.html', {
            'error': 'Please enter a city'
        })

    api_key = '55499e21527e64b1003e1adbc992736d'

    url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 200:

            WeatherData.objects.create(
                city = data['name'],
                temperature = data['main']['temp'],
                description = data['weather'][0]['description'],
                humidity = data['main']['humidity']

            )

            context = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity']
            }

        else:

            context = {
                'error': 'City not found'
            }

    except requests.exceptions.RequestException:
        context = {
            'error': 'Unable to connect to weather API. Check your internet connection.'
        }

    return render(request, 'weather.html', context)
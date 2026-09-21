import requests
from django.shortcuts import render


def weather(request):

    city = request.GET.get('city', 'Hyderabad')

    api_key = '55499e21527e64b1003e1adbc992736d'

    url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(url, params=params)

    data = response.json()

    if response.status_code == 200:
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

    return render(request, 'weather.html', context)
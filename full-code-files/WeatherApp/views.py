""" This app allows the user to see the current weather for the location of
their choosing. They can either enter a city or a US zip code. The zip code
will be given priority if they enter both. """

import requests
import json
from django.shortcuts import render
from .forms import ZipForm, CityForm

# core variables for requests:
units = 'imperial'
country = 'us'
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather"
# Enter API key here - limited attempts in free access so may need to make new account if not working
api_key = "717773b8d51cee768b8ceb819ad9aeb3"


def weather(request):
    # For initial call when no data has been entered
    if request.method == 'GET':
        form1 = ZipForm(initial={'zip': 'Zip Code',})
        form2 = CityForm(initial={'city': 'City Name'})
        location = {'form1': form1, 'form2': form2}
        return render(request, 'Weather/weather.html', location)

    # For when data has been entered
    elif request.method == 'POST':
        form1 = ZipForm(request.POST)
        form2 = CityForm(request.POST)
        
        # validating and cleaning data for use
        if form1.is_valid() and form2.is_valid():
            form_zip = form1.cleaned_data
            form_city = form2.cleaned_data
            city_name = form_city['city']
            zip_code = form_zip['zip']
        else:
            error = {"not_found": "Invalid Entry: Please Re-enter Location Information."}
            return render(request, "weather/weather.html", {'error': error, 'form1': ZipForm(), 'form2': CityForm()})
        print("ZIP CODE =", zip_code)
        print("CITY IS =", city_name)

    # try zip then city, move directly to city if no zip is entered    
    if zip_code != '' or city_name != '':
        try:
            response = GetZip(zip_code)
            # convert json format data into python format data
            x = response.json()
        except:
            try:
                response = GetCity(city_name)
                x = response.json()
            except:
                error = {"not_found": "City Not Found: Please Re-enter Location Information"}
                return render(request, "weather/weather.html", {'error': error, 'form1': ZipForm(), 'form2': CityForm()})
    else: # if they didn't enter anything return a different error
        error = {"not_found": "Invalid Entry: Please Re-enter Location Information."}
        return render(request, "weather/weather.html", {'error': error, 'form1': ZipForm(), 'form2': CityForm()})

    current_info = GetWeatherInfo(x)
    print(current_info)

    return render(request, "weather/weather.html", {'current_info': current_info, 'form1': ZipForm(), 'form2': CityForm()})


def GetZip(zip_code):
    data = {
        'units': units,
        'appid': api_key,
        'zip': str(zip_code) + ',' + country
        }
    response = requests.get(base_url, params=data)
    if response.status_code == 200:
        return response


def GetCity(city_name):
    data = {
        'units': units,
        'appid': api_key,
        'q': str(city_name)
        }
    response = requests.get(base_url, params=data)
    if response.status_code == 200:
        return response


def GetWeatherInfo(x):
    # Now x contains all the url info in dictionary form
    # Simplifying the calls into the dictionary with y
    y = x['main']
    z = x['weather']
    w = x['wind']

    # Grabbing info of interest to display in forms
    location = x['name']
    current_temp = y["temp"]
    current_humidity = y['humidity']
    weather_description = z[0]['description']
    description = weather_description.title
    weather_icon = z[0]['icon']
    wind_speed = w['speed']

    icon_url = "http://openweathermap.org/img/w/{}.png".format(weather_icon)

    # Put it all together into a dictionary
    current_info = {"location": location, "current_temp": current_temp, "current_humidity": current_humidity,
                    "description": description, "icon": icon_url, "wind_speed": wind_speed}
    return current_info

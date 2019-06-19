""" This app allows the user to see the current weather for the location of
their choosing. They can either enter a city or a US zip code. The zip code
will be given priority if they enter both. """

import requests
import json
from django.shortcuts import render

from .models import Zip, City
from .forms import ZipForm, CityForm


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
        form1.save()
        form2.save()

    # Reset the forms
    form1 = ZipForm()
    form2 = CityForm()

    # Grabs the entry for the city and for the zip code - printing to console just to double-check
    city_name = City.objects.filter()[0]
    zip_code = Zip.objects.filter()[0]
    print("ZIP CODE =", zip_code)
    print("CITY IS = ", city_name)

    # Enter API key here - limited attempts in free access so may need to make new account if not working
    api_key = "717773b8d51cee768b8ceb819ad9aeb3"
    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?units=imperial&"
    # complete_url variable for user specific url lookup - give zip code entry priority
    complete_url = base_url + "appid=" + api_key + "&zip=" + str(zip_code) + ",us"

    # get data from the url
    response = requests.get(complete_url)

    # convert json format data into python format data
    x = response.json()

    # Now x contains all the url info in dictionary form
    # Check the value of "cod" key isn't 404/400 aka location not found/invalid entry
    if x["cod"] != "404" and x['cod'] != "400":

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

        icon_url = "http://openweathermap.org/img/w/" + weather_icon + ".png"

        # Put it all together into a dictionary
        current_info = {"location": location, "current_temp": current_temp, "current_humidity": current_humidity,
                        "description": description, "icon": icon_url, "wind_speed": wind_speed}
        # Create 'context' to return at the end
        context = {'current_info': current_info, 'form1': form1, 'form2': form2}

    # If the Zip Code does return a 404, this prompts it to check the city name entered
    else:
        complete_url = base_url + "appid=" + api_key + "&q=" + str(city_name)
        # Get new values based on city name rather than faulty zip code
        response = requests.get(complete_url)
        x = response.json()

        # If city name returns info, create context to return to user
        if x["cod"] != "404" and x['cod'] != '400':
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

            icon_url = "http://openweathermap.org/img/w/" + weather_icon + ".png"
            current_info = {"location": location, "current_temp": current_temp, "current_humidity": current_humidity,
                            "description": description, "icon": icon_url, "wind_speed": wind_speed}
            context = {'current_info': current_info, 'form1': form1, 'form2': form2}

        # If city name also returns a 404/400, return the error to the user
        else:
            error = {"not_found": "City Not Found: Please Re-enter Location Information"}
            context = {'error': error, 'form1': form1, 'form2': form2}

    # Clears out the tables Zip and City to prevent them from growing indefinitely
    Zip.objects.all().delete()
    City.objects.all().delete()

    return render(request, "weather/weather.html", context)



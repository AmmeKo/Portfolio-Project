from django.shortcuts import render

import requests
import xmltodict
from .forms import CountryForm
from bs4 import BeautifulSoup


def advisory(request):

    # providing clear form when user has not entered information
    if request.method == 'GET':
        form = CountryForm()
        return render(request, 'Advisory/advisory.html', {'form': form})

    # if the user has provided info (method == 'POST')
    else:
        form_input = CountryForm(request.POST)

        # validating and cleaning data for use
        if form_input.is_valid():
            form = form_input.cleaned_data
        else:
            error_message = 'Please enter a country name.'
            return render(request, 'Advisory/advisory.html', {'form': CountryForm(), 'error': error_message})

        # grabbing user input for country, alter data to fit - all country names capitalized in url data
        country = form['country'].title()
        
        # url with information from state department on travel warnings
        url = 'https://travel.state.gov/_res/rss/TAsTWs.xml'
        # getting data from url
        r = requests.get(url)
        
        # in case travel.state.gov is down
        if r.status_code != 200:
            print(r.status_code)
            error_message = 'The server is currently unavailable. Please try again later. If problem persists, contact administrator.'
            return render(request, 'Advisory/advisory.html', {'form': CountryForm(), 'error': error_message})

        # parsing data into dictionary form (from xml) and
        # grabbing information on the actual countries out of the dictionary for easier access below
        data = xmltodict.parse(r.content)
        x = data['rss']['channel']['item']

        # scanning through the dictionary for the country chosen by the user and grabbing that country's data
        country_info = ''
        for item in x:
            if country in "'+{}+'".format(item['title']):
                country_info = item
                break

        # in case the country cannot be found
        if country_info == '':
            error_message = 'No information on \"{}\" could be found at this time. Please check that the ' \
                           'country name is spelled correctly and try again.'.format(country)
            return render(request, 'Advisory/advisory.html', {'form': CountryForm(), 'error': error_message})

        title_full = country_info['title']
        # removing country name from title so it can be displayed more prominently elsewhere
        title = title_full.replace(country+' - ', '')
        date = country_info['pubDate']
        link = country_info['link']
        description_html = country_info['description']
        # parsing out the long description and grabbing the initial paragraph's text to present to user
        description_long = BeautifulSoup(description_html, features='html.parser')
        description = description_long.p.text

        # scanning through the country data info (it's title) to grab the warning level. Levels range from 1-4
        for i in range(1,5):
            if 'Level {}'.format(i) in country_info['title']:
                alert_level = i
                break
        # assigning color based on alert level for in-line styling for background and font on the html section
        alert = {
            1: {'color': 'DarkBlue', 'font': 'White'},
            2: {'color': 'Yellow', 'font': 'Black'},
            3: {'color': 'Orange', 'font': 'Black'},
            4: {'color': 'Red', 'font': 'Black'}
            }
        alert_color = alert[alert_level]['color']
        alert_font = alert[alert_level]['font']

        # compiling data to be sent back to html
        warning_info = {'country': country, 'title': title, 'date': date, 'link': link, 'description': description,
                        'alert_color': alert_color, 'font_color': alert_font}

        # returning information to be displayed and blank form
        return render(request, 'Advisory/advisory.html', {'form': CountryForm(), 'info': warning_info})

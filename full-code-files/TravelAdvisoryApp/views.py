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
        form = CountryForm(request.POST)

        # validating and cleaning data for use
        if form.is_valid():
            form = form.cleaned_data

        # grabbing user input for country
        country = form['country']
        # alter data to fit - all country names capitalized in url data
        country = country.capitalize()

        # url with information from state department on travel warnings
        url = 'https://travel.state.gov/_res/rss/TAsTWs.xml'

        # getting data from url and then parsing it into a dictionary form (from xml)
        r = requests.get(url)
        data = xmltodict.parse(r.content)
        # grabbing information on the actual countries out of the dictionary for easier access below
        x = data['rss']['channel']['item']

        # scanning through the dictionary for the country chosen by the user and grabbing that country's data
        country_info = ''
        i = 0
        for item in x:
            if country in "'+{}+'".format(x[i]['title']):
                country_info = x[i]
            i += 1

        # in case the country cannot be found
        if country_info == '':
            error_message = 'No information on {} could be found at this time. Please check that the ' \
                           'country name is spelled correctly and try again.'.format(country)
            print(error_message)
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
        i = 1
        while i < 5:
            if 'Level {}'.format(i) in country_info['title']:
                alert_level = i
            i += 1
        # assigning color based on alert level for in-line styling for background and font on the html section
        if alert_level == 1:
            alert_color = 'DarkBlue'
            font_color = 'White'
        elif alert_level == 2:
            alert_color = 'Yellow'
            font_color = 'Black'
        elif alert_level == 3:
            alert_color = 'Orange'
            font_color = 'Black'
        elif alert_level == 4:
            alert_color = 'Red'
            font_color = 'Black'

        warning_info = {'country': country, 'title': title, 'date': date, 'link': link, 'description': description,
                        'alert_color': alert_color, 'font_color': font_color}

        # returning information to be displayed and blank form
        return render(request, 'Advisory/advisory.html', {'form': CountryForm(), 'info': warning_info})
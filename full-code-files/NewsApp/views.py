from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import SearchForm
import ast
import requests
import datetime
import json

import urllib.request


def news_data(request):

    # if a GET (or any other method) we'll create a blank form
    if request.method == 'GET':
        search_form = SearchForm()

        # put in a url with top headlines for today US to populate the initial page
        url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=b21c9ca0b07c4a1e950b725f85ca4ad2'
        response = requests.get(url)
        x = response.json()
        message = 'Top News Stories in the USA Today:'
        # grabbing article info out of response from NewsApi
        articles = x['articles']
        art_list = []
        i = 0
        # iterating through the dictionary of info on the articles for relevant info and putting into list to return
        for article in articles:
            y = articles[i]
            title = y['title']
            description = y['description']
            image = y['urlToImage']
            link = y['url']
            date_pub = datetime.datetime.strptime(y['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            date = date_pub.date()
            info_list = [i+1, title, description, image, link, date]
            art_list.append(info_list)
            i = i + 1
        # return form, message, and info on articles to the html page
        return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'message': message, 'list': art_list})

    # if this is a POST request we need gather/process the form data
    else:
        search_form = SearchForm(request.POST)

        # Validate the form and return clean data
        if search_form.is_valid():
            form = search_form.cleaned_data
        else:
            error_message = 'Unable to process your request. Please try again. If problem persists, contact administrator.'
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'error': error_message})

        # set up base_url depending on if it's a headline search or not
        if form['search_type'] == 'True':
            base_url = 'https://newsapi.org/v2/top-headlines?'
        else:
            base_url = 'https://newsapi.org/v2/everything?'

        # grab the search data
        key_words = form['key_words']
        start_date = form['date_earliest']
        end_date = form['date_latest']
        sort = form['sort']
        sources = form['sources']

        # parse sources into proper string for url if any were entered
        if sources != '':
            src_list = ast.literal_eval(sources)
            sources = ','.join(src_list)

        api_key = 'b21c9ca0b07c4a1e950b725f85ca4ad2'

        # format full url for query using input
        url = '{}q={}&from={}&to={}&sources={}&sortBy={}&apiKey={}'\
            .format(base_url, key_words, start_date, end_date, sources, sort, api_key)

        # get data from the url
        response = requests.get(url)

        # convert json format data into python format data
        x = response.json()

        # check for errors in query to determine response to user
        if x['status'] == 'ok':  # no errors detected
            message = 'Your search returned ' + str(x['totalResults']) + ' results.'
            articles = x['articles']
            art_list = []
            # setting up an int for index value in articles
            i = 0
            # iterating through the dictionary of info on the articles for relevant info and putting into list to return
            for article in articles:
                y = articles[i]
                title = y['title']
                description = y['description']
                image = y['urlToImage']
                link = y['url']
                date_pub = datetime.datetime.strptime(y['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                date = date_pub.date()
                info_list = [i+1, title, description, image, link, date]
                art_list.append(info_list)
                i = i + 1
            # return form, message, and info on articles to the html page
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'message': message, 'list': art_list})

        elif x['status'] == 'error':  # checking for 2 main errors to provide proper message to user
            if x['code'] == 'parametersMissing':
                error_message = 'Please enter a keyword and/or select news source.'
            elif x['code'] == 'apiKeyInvalid':
                error_message = 'Your API Key is invalid. Please go to https://newsapi.org to register.'
            else:  # this should only occur if the url is faulty
                error_message = 'Your search is invalid. Please try again. If problem persists, contact administrator.'
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'error': error_message})

        else:  # if status returns an unknown value - should not occur unless url is faulty
            error_message = 'Your search is invalid. Please try again. If problem persists, contact administrator.'
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'error': error_message})

    return render(request, 'AppDemoNews/news_data.html', {'form': search_form})

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
        # iterating through the dictionary of info on the articles for relevant info and putting into list to return
        for article in articles:
            title = article['title']
            description = article['description']
            image = article['urlToImage']
            link = article['url']
            try:
                date_pub = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                date = date_pub.date()
            except:
                date = 'N/A'
            i = articles.index(article) + 1
            info_list = [i, title, description, image, link, date]
            art_list.append(info_list)
        # return form, message, and info on articles to the html page
        return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'message': message, 'list': art_list})

    # if this is a POST request we need gather/process the form data
    else:
        search_form = SearchForm(request.POST)

        # Validate the form and return clean data
        if search_form.is_valid():
            form = search_form.cleaned_data
        else:
            error_message = 'Your search parameters are invalid. Please try again. If problem persists, contact administrator.'
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'error': error_message})

        # set up base_url depending on if it's a headline search or not
        if form['headlines'] == 'True':
            base_url = 'https://newsapi.org/v2/top-headlines'
        else:
            base_url = 'https://newsapi.org/v2/everything'

        # sources come in as a list in string form and need to be a string with sources separated by commas
        # parse sources into proper string for url if any were entered
        sources = form['sources']
        if sources != '':
            src_list = ast.literal_eval(sources)
            sources = ','.join(src_list)
        
        # grab the search data
        data = {
            'q': form['key_words'],
            'from': form['date_earliest'],
            'to': form['date_latest'],
            'sources': sources,
            'sortBy': form['sort'],
            'apiKey': 'b21c9ca0b07c4a1e950b725f85ca4ad2'
            }
        
        # get data from the url
        response = requests.get(base_url, params=data)
        # convert json format data into python format data
        x = response.json()
        
        # check for errors in query to determine response to user
        if response.status_code == 200:  # no errors detected        
            message = 'Your search returned {} results.'.format(str(x['totalResults']))
            articles = x['articles']
            art_list = []
            # iterating through the dictionary of info on the articles for relevant info and putting into list to return
            for article in articles:
                title = article['title']
                description = article['description']
                image = article['urlToImage']
                link = article['url']
                try:
                    date_pub = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                    date = date_pub.date()
                except:
                    date = 'N/A'
                i = articles.index(article) + 1
                info_list = [i, title, description, image, link, date]
                art_list.append(info_list)
            # return form, message, and info on articles to the html page
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'message': message, 'list': art_list})

        elif response.status_code == 400:  # checking for 3 specific errors to provide proper message to user
            error_message = 'Please enter a keyword and/or select news source.'
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'error': error_message})
        elif response.status_code == 401:
            error_message = 'Your API Key is invalid. Please go to https://newsapi.org to register.'
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'error': error_message})
        elif response.status_code == 429:
            error_message = 'Too many requests have been made. Please come back and try your search again later.'
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'error': error_message})

        else:
            error_message = 'There has been a server error. Please try again. If problem persists, contact administrator.'
            return render(request, 'AppDemoNews/news_data.html', {'form': search_form, 'error': error_message})

    return render(request, 'AppDemoNews/news_data.html', {'form': search_form})

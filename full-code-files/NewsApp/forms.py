from django import forms
import datetime


class SearchForm(forms.Form):
    SOURCE_CHOICES = (('abc-news', 'ABC News'), ('al-jazeera-english', 'Al Jazeera'), ('bbc-news', 'BBC News'),
                    ('cbs-news', 'CBS News'), ('cnn', 'CNN'), ('the-huffington-post', 'Huffington Post'),
                    ('nbc-news', 'NBC News'), ('the-new-york-times', 'New York Times'),
                    ('the-wall-street-journal', 'Wall Street Journal'), ('the-washington-post', 'Washington Post'),
                    ('usa-today', 'USA Today'), ('espn', 'ESPN'))
    SORT_CHOICES = (('date', 'Date Published'), ('popularity', 'Popularity'), ('relevance', 'Relevance'))

    key_words = forms.CharField(label='Key Words', max_length=100, required=False)
    # The free plan only allows for 1 month worth of news archives - can go further back with paid API KEY
    date_earliest = forms.DateField(label='From', widget=forms.SelectDateWidget(years=range(2019, datetime.date.today().year+1)), required=False)
    date_latest = forms.DateField(label='To', widget=forms.SelectDateWidget(years=range(2019, datetime.date.today().year+1)), required=False)
    sources = forms.CharField(label='Select News Sources', widget=forms.CheckboxSelectMultiple(choices=SOURCE_CHOICES), required=False)
    sort = forms.CharField(label="Sort By", widget=forms.RadioSelect(choices=SORT_CHOICES), required=False)
    search_type = forms.CharField(label="Select to search only today's Top Headlines", widget=forms.CheckboxInput, required=False)

    def clean(self):
        clean_form = self.cleaned_data
        return clean_form

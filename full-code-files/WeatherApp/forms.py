from django.forms import ModelForm, TextInput
from .models import Zip, City


class ZipForm(ModelForm):
    class Meta:
        model = Zip
        fields = ('zip',)
        widgets = {'zip': TextInput(attrs={'class': 'input', 'placeholder': 'Zip Code', 'required': False})}

    def clean(self):
        clean_zip = self.cleaned_data
        return clean_zip


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ('city',)
        widgets = {'city': TextInput(attrs={'class': 'input', 'placeholder': 'City Name', 'required': False})}

    def clean(self):
        clean_city = self.cleaned_data
        return clean_city

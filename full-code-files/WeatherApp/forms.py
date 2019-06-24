from django import forms


class ZipForm(forms.Form):
    zip = forms.CharField(max_length=5, required=False)    

    def clean(self):
        clean_zip = self.cleaned_data
        return clean_zip


class CityForm(forms.Form):
    city = forms.CharField(max_length=50, required=False)

    def clean(self):
        clean_city = self.cleaned_data
        return clean_city

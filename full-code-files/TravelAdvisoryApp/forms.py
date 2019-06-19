from django import forms


class CountryForm(forms.Form):
    country = forms.CharField(label='Enter Country Name', max_length=50, required=True)

    def clean(self):
        clean_form = self.cleaned_data
        return clean_form
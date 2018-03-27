from django import forms
import requests
import json

class LogInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
'''
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        d = {'username': username, 'password': password}
        x = requests.post('http://exp-api:8000/services/users/login', d)
        resp_json = x.json()
        #resp = json.loads(resp_json)
        if not resp_json or 'error' in resp_json:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data
'''
class CreateNewItemForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    price = forms.DecimalField(max_digits=6, decimal_places=2)
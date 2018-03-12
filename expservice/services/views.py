from django.shortcuts import render
from django.http import JsonResponse
#from bakery.models import User, Item

# Create your views here.

import urllib.request
import urllib.parse
import json

# home page
def latestUsers(request):

def latestItems(request):

# item details
"""
def userDetails(request, username):
    name = str(username)
    url = 'http://models-api/api/v1/users/' + name + '/'
    with urllib.request.urlopen(url) as response:
        json = response.read()
    encoding = json.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))
    return JSON_object
"""
def itemDetails(request, item_name, username):
    item_name = str(item_name)
    name = str(username)
    url = 'http://models-api/api/v1/users/' + name + '/' + item_name + '/'
    with urllib.request.urlopen(url) as response:
        json = response.read()
    encoding = json.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))
    return JSON_object

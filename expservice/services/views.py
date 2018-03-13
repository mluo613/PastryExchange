from django.shortcuts import render
from django.http import JsonResponse
#from bakery.models import User, Item

# Create your views here.

import urllib.request
import urllib.parse
import json

# home page
#def latestUsers(request):

def latestItems(request):
    url = 'http://models-api/api/v1/getallitems'
    with urllib.request.urlopen(url) as response:
        json = response.read()

    newList = json[-5:]
    encoding = newList.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))
    return JSON_object
"""
    encoding = json.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))
    newList = JSON_object[-5:]
    newJSON_object = json.loads(newList)
"""
   # return newJSON_object

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

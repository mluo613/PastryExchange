from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests


# Create your views here.

import urllib.request
import urllib.parse
import json

# home page
def latestItems(request):
    url = 'http://models-api:8000/api/v1/getallitems'
    req = urllib.request.Request(url)

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    r2 = json.JSONDecoder().decode(resp_json)

    newList = r2[-5:]
    return JsonResponse(newList, safe=False)

def itemDetails(request, pk):
    try:
        key = str(pk)
        url = 'http://models-api:8000/api/v1/items/' + key
        req = urllib.request.Request(url)
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        r2 = json.JSONDecoder().decode(resp_json)
        return JsonResponse(r2, safe=False)
    except:
        return JsonResponse("Something went wrong!", safe=False)

def createAccount(request):
#    try:
        data_dict = request.POST
        #data_encoded = urllib.urlencode(data_dict)
        url = 'http://models-api:8000/api/v1/users/create$'
        #req = urllib.request.Request(url, data_encoded)
        #resp = urllib.request.urlopen(req).read().decode('utf-8')
        resp = requests.post(url, data_dict)
        #resp_json = json.JSONDecoder().decode(resp)
        resp_json = resp.json()
        return JsonResponse(resp_json, safe=False)
        #return JsonResponse("It worked!", safe=False)
#    except:
#        return JsonResponse("Something went wrong!", safe=False)

def logout(request):
#    try:
        data_dict = request.POST
        #data_encoded = urllib.urlencode(data_dict)
        url = 'http://models-api:8000/api/v1/users/logout'
        #req = urllib.request.Request(url, data_encoded)
        #resp = urllib.request.urlopen(req).read().decode('utf-8')
        resp = requests.post(url, data_dict)
        #resp_json = json.JSONDecoder().decode(resp)
        resp_json = resp.json()
        return JsonResponse(resp_json, safe=False)
        #return JsonResponse("It worked!", safe=False)
#    except:
#        return JsonResponse("Something went wrong!", safe=False)

def login(request):
#    try:
    data_dict = request.POST
    #data_encoded = urllib.urlencode(data_dict)
    url = 'http://models-api:8000/api/v1/users/login'
    #req = urllib.request.Request(url, data_encoded)
    #resp = urllib.request.urlopen(req).read().decode('utf-8')
    resp = requests.post(url, data_dict)
    #resp_json = json.JSONDecoder().decode(resp)
    resp_json = resp.json()
    return JsonResponse(resp_json, safe=False)
    #return JsonResponse("It worked!", safe=False)
#    except:
#        return JsonResponse("Something went wrong!", safe=False)

def create_new_item(request, username):
#    try:
        data_dict = request.POST
        #data_encoded = urllib.urlencode(data_dict)
        url = 'http://models-api:8000/api/v1/users/' + str(username) + '/uploadItem'
        #req = urllib.request.Request(url, data_encoded)
        #resp = urllib.request.urlopen(req).read().decode('utf-8')
        resp = requests.post(url, data)
        #resp_json = json.JSONDecoder().decode(resp)
        resp_json = resp.json()
        return JsonResponse(resp_json, safe=False)
        #return JsonResponse("It worked!", safe=False)
#    except:
#        return JsonResponse("Something went wrong!", safe=False)
    

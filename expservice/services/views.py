from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

import urllib.request
import urllib.parse
import json

# home page
def latestItems(request):
#    try:
    url = 'http://models-api:8000/api/v1/getallitems'
    req = urllib.request.Request(url)

    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    r2 = json.JSONDecoder().decode(resp_json)

    newList = r2[-5:]
    return JsonResponse(newList, safe=False)
#    except:
#        return JsonResponse("Something went wrong!", safe=False)

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
    try:
        url = 'http://models-api:8000/api/v1/users/create$'
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req).read().decode('utf-8')
        resp_json = json.JSONDecoder().decode(resp)
        return JsonResponse(resp_json, safe=False)
        #return JsonResponse("It worked!", safe=False)
    except:
        return JsonResponse("Something went wrong!", safe=False)

def logout(request):
    try:
        url = 'http://models-api:8000/api/v1/users/logout'
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req).read().decode('utf-8')
        resp_json = json.JSONDecoder().decode(resp)
        return JsonResponse(resp_json, safe=False)
        #return JsonResponse("It worked!", safe=False)
    except:
        return JsonResponse("Something went wrong!", safe=False)

def login(request):
    try:
        url = 'http://models-api:8000/api/v1/users/login$'
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req).read().decode('utf-8')
        resp_json = json.JSONDecoder().decode(resp)
        return JsonResponse(resp_json, safe=False)
        #return JsonResponse("It worked!", safe=False)
    except:
        return JsonResponse("Something went wrong!", safe=False)

def create_new_item(request):
    try:
        url = 'http://models-api:8000/' #add url
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req).read().decode('utf-8')
        resp_json = json.JSONDecoder().decode(resp)
        #return JsonResponse(resp_json, safe=False)
        return JsonResponse("It worked!", safe=False)
    except:
        return JsonResponse("Something went wrong!", safe=False)
    

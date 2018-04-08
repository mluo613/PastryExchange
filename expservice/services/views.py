from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
from elasticsearch import Elasticsearch
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json


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
    data_dict = request.POST
    url = 'http://models-api:8000/api/v1/users/create'
    resp = requests.post(url, data_dict)
    resp_json = resp.json()
    return JsonResponse(resp_json, safe=False)

def logout(request):
    data_dict = request.POST
    url = 'http://models-api:8000/api/v1/users/logout'
    resp = requests.post(url, data_dict)
    resp_json = resp.json()
    return JsonResponse(resp_json, safe=False)

def login(request):
    data_dict = request.POST
    url = 'http://models-api:8000/api/v1/users/login'
    resp = requests.post(url, data_dict)
    resp_json = resp.json()
    return JsonResponse(resp_json, safe=False)

def create_new_item(request):
    data_dict = request.POST
    url = 'http://models-api:8000/api/v1/users/uploadItem'
    resp = requests.post(url, data_dict)
    resp_json = resp.json()
    if resp_json['status'] == False:
        return JsonResponse(resp_json, safe=False)
    else:
       item_details = itemDetails(request, resp_json['item_id'])
       producer = KafkaProducer(bootstrap_servers='kafka:9092')
       producer.send('new-listings-topic', json.dumps(item_details).encode('utf-8'))
       return JsonResponse(resp_json, safe=False)

# search

def search_items(request, query):
    es = Elasticsearch(['es'])
    term = str(query)
    results = es.search(index='listing_index', body={'query': {'query_string': {'query': term}}, 'size':10})
    return JsonResponse(results, safe=False)

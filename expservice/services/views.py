from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
from elasticsearch import Elasticsearch
from kafka import KafkaProducer


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

def itemDetails(request, pk, auth):
    #try:
        key = str(pk)
        url = 'http://models-api:8000/api/v1/items/' + key + '/' + auth
        req = urllib.request.Request(url)
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        r2 = json.JSONDecoder().decode(resp_json)

        # need to set a cookie that stores username when logged in. In this method, call a method(not written yet) that checks for cookie exist, if so publish to kafka
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        if r2[0]['username']!='None':
            producer.send('item-detail-topic', json.dumps(r2).encode('utf-8'))

        newList = []
        final_json = {'itemInfo':r2, 'recs':[]}
        if r2[0]['status']==True:
            new_url = 'http://models-api:8000/api/v1/recs/' + r2[0]['item_id']
            new_req = urllib.request.Request(new_url)
            new_resp_json = urllib.request.urlopen(new_req).read().decode('utf-8')
            recs = json.JSONDecoder().decode(new_resp_json)
            recslist = recs[0]['recommended_items'].split(",")
            for i in recslist:
                try:
                    num = i.strip('\'')
                    req1 = urllib.request.Request('http://models-api:8000/api/v1/items/'+str(num)+'/None')
                    resp1 = urllib.request.urlopen(req1).read().decode('utf-8')
                    details = json.JSONDecoder().decode(resp1)
                    newList.append(details)
                except:
                    newList.append(0)
            newList = newList[-5:]

        final_json['recs'].append(newList)

        return JsonResponse(final_json, safe=False)
    #except:
    #    return JsonResponse("Something went wrong!", safe=False)

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
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    if resp_json['status']==True:
       producer.send('new-listings-topic', json.dumps(resp_json).encode('utf-8'))
    return JsonResponse(resp_json, safe=False)

def update_item(request, pk):
    data_dict = request.POST
    item_id = str(pk)
    url = 'http://models-api:8000/api/v1/items/updateItem/' + item_id
    resp = requests.post(url, data_dict)
    resp_json = resp.json()
    return JsonResponse(resp_json, safe=False)

def delete_item(request, pk):
    data_dict = request.POST
    item_id = str(pk)
    url = 'http://models-api:8000/api/v1/items/deleteItem/' + item_id
    resp = requests.post(url, data_dict)
    resp_json = resp.json()
    return JsonResponse(resp_json, safe=False)

def update_user(request):
    data_dict = request.POST
    url = 'http://models-api:8000/api/v1/users/update'
    resp = requests.post(url, data_dict)
    resp_json = resp.json()
    return JsonResponse(resp_json, safe=False)

def delete_user(request):
    data_dict = request.POST
    url = 'http://models-api:8000/api/v1/users/delete'
    resp = requests.post(url, data_dict)
    resp_json = resp.json()
    return JsonResponse(resp_json, safe=False)

# search

def search_items(request, query):
    es = Elasticsearch(['es'])        
    term = str(query)
    results = es.search(index='listing_index', body={'query': {'query_string': {'query': term}}, 'size':10})
    return JsonResponse(results, safe=False)

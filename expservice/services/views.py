from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

import urllib.request
import urllib.parse
import json

# home page
def latestItems(request):
    try:
        url = 'http://models-api:8000/api/v1/getallitems/'
        
        with urllib.request.urlopen(url) as response:
            json = response.read()

            encoding = json.info().get_content_charset('utf-8')
            JSON_object = json.loads(data.decode(encoding))
            newList = JSON_object[-5:]
            newJSON_object = json.loads(newList)
            return newJSON_object
    except:
        return JsonResponse("Something went wrong!", safe=False)

# details 
def itemDetails(request, pk):
    if request.method == 'GET':
#        try:
            key = str(pk)
            url = 'http://models-api:8000/api/v1/items/' + key
            
            req = urllib.request.Request(url)
            
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            #return JsonResponse("Something2.", safe=False)
            #resp = json.loads(resp_json)
            #with urllib.request.urlopen(url) as response:
             #   json = response.read()
            #encoding = json.info().get_content_charset('utf-8') 
            #JSON_object = json.loads(data.decode(encoding))                                                                                                                                                         
            #return JSON_object
            return JsonResponse(json.JSONDecoder().decode(resp_json), safe=False)
            #return resp_json

#        except:
#            return JsonResponse("Something went wrong.", safe=False)


"""                                                                                                                                                                   
                                                                                                                                                                      
            with urllib.request.urlopen(url) as response:                                                                                                             
                json = response.read()                                                                                                                                
            encoding = json.info().get_content_charset('utf-8')                                                                                                       
            JSON_object = json.loads(data.decode(encoding))                                                                                                           
            return JSON_object                                                                                                                                        
"""

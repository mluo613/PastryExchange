from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import HttpResponse


# Create your views here.
def bakeryItemDetails(request, pk):
    try:
        req = urllib.request.Request('http://exp-api:8000/services/bakeryItem/' + str(pk) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        #r1 = urllib.request.urlopen(req)
        #return HttpResponse("Page.")
        #r2 = r1.read()
        #return HttpResponse("Page2.")
        #r3 = r2.decode('utf-8')
        #return HttpResponse("Page3.")
        resp = json.loads(resp_json)
        return HttpResponse(resp_json)
        #d = dict(resp)
        if resp == "Something went wrong!" or resp == "Item does not exist.":
            return HttpResponse("Item does not exist.")
        
        context = {
            'bakeryItem' : resp_json,
            }
        return render(request, 'bakery/bakeryItem_detail.html', context)
    except:
        return HttpResponse("Page does not exist.")

def index(request):
    try:
        req = urllib.request.Request('http://exp-api:8000/services/latestItems/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        #if resp == "Something went wrong!" or resp == "Item does not exist.":
        #return HttpResponse(resp)    
        context = {
            'bakeryItem_list': resp,
            }
        return render(request, 'bakery/index.html', context)

    except:
        return HttpResponse("Page does not exist.")

#class bakeryItemListView(generic.ListView):
 #   model = bakeryItem

#class bakeryItemDetailView(generic.DetailView):
 #   model = bakeryItem

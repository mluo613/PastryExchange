from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import HttpResponse

# Create your views here.
def bakeryItemDetails(request, pk):
    try:
        req = urllib.request.Request('http://exp-api:8000/bakeryItem/' + str(pk) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        context = {
            'bakeryItem': resp,
            }
        return render(request, 'bakery/bakeryItem_detail.html', context)
    except:
        return HttpResponse("Page does not exist.")

def index(request):
    try:
        req = urllib.request.Request('http://exp-api:8000/latestItems/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        if resp == "Something went wrong!":
            
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

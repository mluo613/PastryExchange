from django.shortcuts import render
import urllib.request
import urllib.parse
import urllib
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import requests

from .forms import LogInForm, CreateNewItemForm
from django.contrib import messages
from django.contrib.messages import get_messages
#import exp_srvc_errors

# Create your views here.

def login(request):
    # If we received a GET request instead of a POST request
    if request.method == 'GET':
        # display the login form page
        next = request.GET.get('next') or reverse('index')
        form = LogInForm()
        return render(request, 'bakery/login.html', {'form': form})

    # Creates a new instance of our login_form and gives it our POST data
    form = LogInForm(request.POST)

    # Check if the form instance is invalid
    if not form.is_valid():
      # Form was bad -- send them back to login page and show them an error
      return render(request, 'bakery/login.html', {'form': form})

    # Sanitize username and password fields
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    d = {'username': username, 'password':password}
    #encoded = urllib.parse.urlencode(d).encode("utf-8")

    # Get next page
    #next =

    # Send validated information to our experience layer
    x = requests.post('http://exp-api:8000/services/users/login', d)
    resp_json = x.json()
    #resp = json.loads(resp_json)
    #req = urllib.request.Request('http://exp-api:8000/services/users/login', encoded)
    #resp_json = urllib.request.urlopen(req).read().decode('utf-8')

    # Check if the experience layer said they gave us incorrect information
    if not resp_json or resp_json['status'] == False:
        # Couldn't log them in, send them back to login page with error
        form = LogInForm()
        return render(request, 'bakery/login.html', {'error': resp_json['message'], 'form': form, 'name': name})

    """ If we made it here, we can log them in. """
    # Set their login cookie and redirect to back to wherever they came from
    #data = form.cleaned_data
    authenticator = resp_json["Auth_num"]

    response = HttpResponseRedirect(reverse('index'))
    response.set_cookie("auth", authenticator)

    return response

def signup(request):
    return render(request, 'bakery/signup.html')

def logout(request):
    auth = request.COOKIES.get('auth')
    d = {'Auth_num': auth}
    x = requests.post('http://exp-api:8000/services/users/logout', d)
    resp_json = x.json()
    #return HttpResponse(resp)
    if not resp_json or resp_json['status'] == False:
        # Couldn't log them in, send them back to login page with error
        form = LogInForm()
        return render(request, 'bakery/login.html', {'error': resp_json['message'], 'form': form})

    #if resp == 'You are logged out.': ; else 'error while logging out' (have this error handling in the logout.html file)

    return render(request, 'bakery/logout.html')


def createNewItem(request):

    # Try to get the authenticator cookie
    auth = request.COOKIES.get('auth')
    #return HttpResponse(auth)

    # If the authenticator cookie wasn't set...
    if not auth:
      # Handle user not logged in while trying to create a listing
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("createNewItem"))

    # If we received a GET request instead of a POST request...
    if request.method == 'GET':
        # Return to form page
        ###next = request.GET.get('next') or reverse('home')
        form = CreateNewItemForm()
        return render(request, 'bakery/createNewItem.html', {'form': form})

    # Otherwise, create a new form instance with our POST data
    form = CreateNewItemForm(request.POST)
    if not form.is_valid():
      # Form was bad -- send them back to login page and show them an error
      return render(request, 'bakery/createNewItem.html', {'form': form})
    # ...

    # Send validated information to our experience layer
    name = form.cleaned_data['name']
    price = form.cleaned_data['price']
    d = {'Auth_num': auth, 'name': name, 'price': price}
    x = requests.post('http://exp-api:8000/services/users/uploadItem', d)
    resp_json = x.json()
    #return HttpResponse(resp_json)
    # Check if the experience layer said they gave us incorrect information
    if not resp_json or resp_json['status'] == False:
        #messages.add_message(request, messages.INFO, resp_json['message'])
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("createNewItem"))

    elif resp_json['status'] == 'reupload':
        form = CreateNewItemForm()
        return render(request, 'bakery/createNewItem.html', {'error': resp_json['message'], 'form': form})

    # ...

    return bakeryItemDetails(request, resp_json['item_id'])

def bakeryItemDetails(request, pk):
    try:
        req = urllib.request.Request('http://exp-api:8000/services/bakeryItem/' + str(pk) + '/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
 #   return HttpResponse(resp)
        if resp == "Something went wrong!" or resp == "Item does not exist.":
            return HttpResponse("Item does not exist.")
        context = {
            'bakeryItem' : resp,
            }
        #return HttpResponse(bakeryItem) 
        return render(request, 'bakery/bakeryItem_detail.html', context)
    except:
        return HttpResponse("Page does not exist.")

def index(request):
    try:
        req = urllib.request.Request('http://exp-api:8000/services/latestItems/')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
  #      return HttpResponse(resp)
        if resp == "Something went wrong!":    
            return HttpResponse("Something went wrong!")
        context = {
            'bakeryItem_list': resp,
            }
        return render(request, 'bakery/index.html', context)

    except:
        return HttpResponse("Page does not exist.")


from django.shortcuts import render
from django.http import JsonResponse
from bakery.models import User, Item, Review

# Create your views here.

import urllib.request
import urllib.parse
import json

from bakery.models import User, Item

def get_user(username):
    resp = views.getUpdate_user('GET', username)
    print (resp)
    return resp

def update_user(username):
    resp = bakery.views.getUpdate_user('POST', username)
    print (resp)
    return resp

def get_item(item_name, username):
    resp = getUpdate_item('GET', item_name, username)
    print (resp)
    return resp

def update_item(item_name, username):
    resp = getUpdate_item('POST', item_name, username)
    print (resp)
    return (resp)

def create_user():
    resp = create_user('POST')
    return resp

def delete_user(username):
    resp = delete_user('POST', username)
    return resp


"""
def users_all(request):
    try:
        users = User.objects.all()
        return JsonResponse(users, safe=False)
    except:
        return JsonResponse("Something went wrong!", safe=False)

def getUserItems(request, username):
    try:
        name = str(username)
        user = User.objects.get(username=name)
        items = User.objects.filter(seller=user)
        return JsonResponse(items, safe=False)
    except:
        return JsonResponse("Error!", safe=False)
    

def items_all(request):
    try:
        items = Item.objects.all()
        return JsonResponse(items, safe=False)
    except:
        return JsonResponse("Something went wrong!", safe=False)

"""

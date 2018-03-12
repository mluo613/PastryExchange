from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from api.v1.models import User, Item

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

def home(request):
    return HttpResponse("This is the home page!")

# These are the functions for the model User

def getUpdate_user(request, username):
    if request.method == 'GET':
        try:
            name = str(username)
            user = User.objects.get(username=name)
            return JsonResponse({"Password":user.password, "Username: ": user.username}, safe=False)
        except:
            return JsonResponse("User does not exist.", safe=False)

    elif request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            user.password = request.POST.get('password')
            user.save()
            return JsonResponse("User exists. Password updated.", safe=False)
        except:
            return JsonResponse("User does not exist.", safe=False)

def create_user(request):
    if request.method == 'POST':
        try:
            user = User.objects.create(username=request.POST.get('username'),
                                       password=request.POST.get('password'))
            user.save()
            return JsonResponse({"Password": user.password, "Username: ": user.username}, safe=False)
        except:
            return JsonResponse("Cannot create user because fields are incorrect or user already exists.")

def delete_user(request, username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            user.delete()
            return JsonResponse("User deleted.", safe=False)
        except:
            return JsonResponse("Cannot delete user because user does not exist.", safe=False)

# These are the functions for model Item
def getUpdate_item(request, item_name, username):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            item = Item.objects.get(name=item_name, seller=user)
            return JsonResponse({"Name":item.name,
                             "Price": item.price,
                             "Date Posted: ": item.datePosted,
                             "Seller": str(item.seller),
                             },
                            safe=False)

        except:
            return JsonResponse("Item does not exist.", safe=False)

    elif request.method == 'POST':
        try:
            item = Item.objects.get(name=item_name)
            if (item.seller.username == username):
                item.price = request.POST.get('price')
                item.save()
                return JsonResponse("Item price updated.", safe=False)
            else:
                return JsonResponse("Item associated with user does not exist.", safe=False)

        except:
            return JsonResponse("Item not found.", safe=False)

'''
        return JsonResponse({"Name":item.name,
                             "Price": item.price,
                             "Date Posted: ": item.datePosted,
                             "Seller": str(item.seller),
                             },
                            safe=False)
'''
def upload_item(request, username):

    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            item = Item.objects.create(name=request.POST.get('name'),
                                       price=request.POST.get('price'),
                                       seller=user)
            item.save()
            return JsonResponse("Item successfully uploaded", safe=False)
        except:
            return JsonResponse("User does not exist. Upload failed.", safe=False)

def delete_item(request, username):

    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            item = Item.objects.get(name=request.POST.get('name'),
                                    seller=user)
            item.delete()
            return JsonResponse("Item successfully deleted", safe=False)
        except:
            return JsonResponse("User or Item does not exist. Delete failed.", safe=False)

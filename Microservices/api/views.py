from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from api.models import User, Item, Authenticator
import json
from django.contrib.auth.hashers import check_password, make_password
import os
import hmac
from django.utils.timezone import utc
import datetime

# import django settings file
from bakery import settings

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

def home(request):
    return HttpResponse("This is the home page!")




# These are the functions for the model User
def login(request):
    '''If password valid, create and returns a authenticator object'''
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST.get('username'))
            valid_pwd = check_password(request.POST.get('password'), user.password)
            try:
                existing_auth = Authenticator.objects.get(user=user)
                return JsonResponse({'status':False,'message':'User already logged in.'}, safe=False)
            except Authenticator.DoesNotExist:
                if valid_pwd:
                    authenticator_random_number = hmac.new(
                        key=settings.SECRET_KEY.encode('utf-8'),
                        msg=os.urandom(32),
                        digestmod='sha256',
                    ).hexdigest()
                    auth = Authenticator.objects.create(auth_num=authenticator_random_number, user=user)
                    auth.save()

                    return JsonResponse(
                        {'status':True,'Auth_num': auth.auth_num, 'user': auth.user.username, 'date': auth.time_added}, safe=False)
                else:
                    return JsonResponse({'status':False, 'message':'Password incorrect.'}, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"status":False, 'message':'User does not exist.'}, safe=False)

def logout(request):
    '''Logs an user out using username'''
    if request.method == 'POST':
        try:
            #user = User.objects.get(username=request.POST.get('username'))
            auth = Authenticator.objects.get(auth_num=request.POST.get('Auth_num'))
            auth.delete()
            return JsonResponse({'status':True,'message':'You are logged out.'}, safe=False)
        #except User.DoesNotExist:
            #return JsonResponse({'status':False,'message':'User does not exist.'}, safe=False)
        except Authenticator.DoesNotExist:
            return JsonResponse({'status':False,'message':'You are already logged out.'}, safe=False)


def get_user(request, username):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            return JsonResponse({"Password":user.password, "Username: ": user.username}, safe=False)
        except:
            return JsonResponse("User does not exist.", safe=False)

def update_user(request):

    if request.method == 'POST':
        try:
            authen = Authenticator.objects.get(auth_num=request.POST.get('Auth_num'))
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - authen.time_added
            time_out_seconds = 60 * 30
            if timediff.total_seconds() > time_out_seconds:
                authen.delete()
                return JsonResponse({'status': False, 'message': 'Login timed out. Please log in again.'}, safe=False)
            userFromAuth = authen.user
            userFromAuth.password = make_password(request.POST.get('password'))
            userFromAuth.save()
            return JsonResponse({'status': True, 'message':"User exists. Password updated."}, safe=False)

        except Authenticator.DoesNotExist:
            return JsonResponse({'status':False, 'message':"User is not logged in. Update failed"}, safe=False)
        except:
            return JsonResponse({'status':False, 'message':'Password update failed.'}, safe=False)

def create_user(request):
    if request.method == 'POST':
        try:
            hash_password = make_password(request.POST.get('password'))
            user = User.objects.create(username=request.POST.get('username'),
                                       password=hash_password)
            user.save()

            authenticator_random_number = hmac.new(
                key=settings.SECRET_KEY.encode('utf-8'),
                msg=os.urandom(32),
                digestmod='sha256',
            ).hexdigest()
            auth = Authenticator.objects.create(auth_num=authenticator_random_number, user=user)
            auth.save()

            return JsonResponse(
                {'status': True, 'Auth_num': auth.auth_num, 'user': auth.user.username, 'date': auth.time_added},
                safe=False)
            #return JsonResponse({'status':True, "Username: ": user.username, 'Password: ': user.password}, safe=False)
        except:
            return JsonResponse({'status':False, 'message':"User already exists."}, safe=False)

def delete_user(request):
    if request.method == 'POST':
        try:
            authen = Authenticator.objects.get(auth_num=request.POST.get('Auth_num'))
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - authen.time_added
            time_out_seconds = 60 * 30
            if timediff.total_seconds() > time_out_seconds:
                authen.delete()
                return JsonResponse({'status': False, 'message': 'Login timed out. Please log in again.'}, safe=False)
            authen.user.delete()
            authen.delete()
            return JsonResponse({'status':True, 'message':"User deleted."}, safe=False)
        except Authenticator.DoesNotExist:
            return JsonResponse({'status':False, 'message':"Cannot delete user because user is not logged in."}, safe=False)

def get_all_users(request):
    if request.method == "GET":
        try:
            userList = User.objects.all()
            results = [ob.as_json() for ob in userList]
            return JsonResponse(json.JSONDecoder().decode(json.dumps(results)),
                                content_type="application/json",
                                safe=False)
        except:
            return JsonResponse("No user in database.", safe=False)

def get_all_logged_users(request):
    if request.method == "GET":
        #try:
        userList = Authenticator.objects.all()
        results = [ob.as_json() for ob in userList]
        return JsonResponse(json.JSONDecoder().decode(json.dumps(results)),
                                content_type="application/json",
                                safe=False)
        #except:
        #    return JsonResponse("No logged user in database.", safe=False)

# These are the functions for model Item
def get_item(request, item_id, auth):
    if request.method == 'GET':
        try:
            item = Item.objects.get(pk=item_id)
            # result = [item.as_json()]
            authObj = Authenticator.objects.get(auth_num=auth)
            # result2 = json.JSONDecoder().decode(json.dumps(result))
            # return JsonResponse(, content_type="application/json", safe=False)
            #
            return JsonResponse([{
                    "item_id":item_id,
                            "name":item.name,
                             "price": item.price,
                             "date posted: ": item.datePosted,
                             "seller": str(item.seller),
                             "username": authObj.user.username
                             }],
                            safe=False)

        except:
            return JsonResponse("Item does not exist.", safe=False)


'''
        return JsonResponse({"Name":item.name,
                             "Price": item.price,
                             "Date Posted: ": item.datePosted,
                             "Seller": str(item.seller),
                             },
                            safe=False)
'''
def update_item(request, item_id):
    if request.method == 'POST':
        try:
            item = Item.objects.get(pk=item_id)
            authen = Authenticator.objects.get(auth_num=request.POST.get('Auth_num'))
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - authen.time_added
            time_out_seconds = 60 * 30
            if timediff.total_seconds() > time_out_seconds:
                authen.delete()
                return JsonResponse({'status': False, 'message': 'Login timed out. Please log in again.'}, safe=False)
            if (item.seller.username == authen.user.username):
                item.price = request.POST.get('price')
                item.name = request.POST.get('name')
                item.save()
                return JsonResponse({'status': True, 'message':"Item's name and price are updated.", 'item_id': item_id}, safe=False)
            else:
                return JsonResponse({'status': False, 'message':"Item is not associated with user. Update failed."}, safe=False)

        except Item.DoesNotExist:
            return JsonResponse({'status': False, 'message':"Item not found."}, safe=False)
        except Authenticator.DoesNotExist:
            return JsonResponse({'status': False, 'message': "User not logged in."}, safe=False)

def upload_item(request):

    if request.method == 'POST':
        try:
            #user = User.objects.get(username=username)
            authen = Authenticator.objects.get(auth_num=request.POST.get('Auth_num'))
            logged_in = (authen.auth_num == request.POST.get('Auth_num'))
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - authen.time_added
            time_out_seconds = 60 * 30
            if timediff.total_seconds() > time_out_seconds:
                authen.delete()
                return JsonResponse({'status': False, 'message': 'Login timed out. Please log in again.'}, safe=False)
            if logged_in:
                item = Item.objects.create(name=request.POST.get('name'),
                                           price=request.POST.get('price'),
                                           seller=authen.user)
                item.save()
                return JsonResponse({'status':True,
                                     'item_id':item.pk,
                                     'seller': item.seller.username,
                                     'name': item.name,
                                     'price': item.price
                                     }, safe=False)
            else:
                return JsonResponse({'status':False, 'message':'Cookie value does not match. Upload failed.'}, safe=False)
        #except User.DoesNotExist:
        #    return JsonResponse({'status':False, 'message':"User does not exist. Upload failed."}, safe=False)
        except Authenticator.DoesNotExist:
            return JsonResponse({'status':False,'message':'User not logged in. Please login before uploading.'}, safe=False)
        #except:
        #    return JsonResponse({'status': 'reupload','message':'Fields of item are incorrect. Upload failed.'}, safe=False)

def delete_item(request, item_id):

    if request.method == 'POST':
        try:
            item = Item.objects.get(pk=item_id)
            authen = Authenticator.objects.get(auth_num=request.POST.get('Auth_num'))
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - authen.time_added
            time_out_seconds = 60 * 30
            if timediff.total_seconds() > time_out_seconds:
                authen.delete()
                return JsonResponse({'status': False, 'message': 'Login timed out. Please log in again.'}, safe=False)
            if authen.user.username == item.seller.username:
                item.delete()
                return JsonResponse({'status': True, 'message': "Item successfully deleted."}, safe=False)
            else:
                return JsonResponse({'status': False, 'message':"Item is not associated with the user. Delete failed."}, safe=False)
        except Item.DoesNotExist:
            return JsonResponse({'status': False, 'message':"Item not found. Delete failed."}, safe=False)
        except Authenticator.DoesNotExist:
            return JsonResponse({'status': False, 'message': "User not logged in. Delete failed."}, safe=False)



def get_all_items(request):
    if request.method == "GET":
        try:
            itemsList = Item.objects.all()
            results = [ob.as_json() for ob in itemsList]
            return JsonResponse(json.JSONDecoder().decode(json.dumps(results)), content_type="application/json", safe=False)
        except:
            return JsonResponse("No items in database.", safe=False)

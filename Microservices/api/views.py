from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from api.models import User, Item, Authenticator
import json
from django.contrib.auth.hashers import check_password, make_password
import os
import hmac
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
                return JsonResponse('User already logged in.', safe=False)
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
                        {'Auth_num': auth.auth_num, 'user': auth.user.username, 'date': auth.time_added}, safe=False)
                else:
                    return JsonResponse({'error':'Password incorrect.'}, safe=False)
        except User.DoesNotExist:
            return JsonResponse({'error':'User does not exist.'}, safe=False)

def logout(request):
    '''Logs an user out using username'''
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST.get('username'))
            auth = Authenticator.objects.get(user=user)
            auth.delete()
            return JsonResponse({'ok':'You are logged out.'}, safe=False)
        except User.DoesNotExist:
            return JsonResponse({'error':'User does not exist.'}, safe=False)
        except Authenticator.DoesNotExist:
            return JsonResponse({'error':'You are already logged out.'}, safe=False)



def getUpdate_user(request, username):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            return JsonResponse({"Password":user.password, "Username: ": user.username}, safe=False)
        except:
            return JsonResponse("User does not exist.", safe=False)
    # Possibly change this to passing in auth?
    elif request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            valid_pwd = check_password(request.POST.get('password'), user.password)
            if valid_pwd:
                user.password = make_password(request.POST.get('newPassword'))
                user.save()
                return JsonResponse("User exists. Password updated.", safe=False)
            else:
                return JsonResponse("Password invalid, thus did not update user profile.", safe=False)
        except User.DoesNotExist:
            return JsonResponse("User does not exist.", safe=False)
        except:
            return JsonResponse('Password update failed due to invalid new password.', safe=False)

def create_user(request):
    if request.method == 'POST':
        try:
            hash_password = make_password(request.POST.get('password'))
            user = User.objects.create(username=request.POST.get('username'),
                                       password=hash_password)
            user.save()
            return JsonResponse({"Username: ": user.username, 'Password: ': user.password}, safe=False)
        except:
            return JsonResponse("User already exists.", safe=False)

def delete_user(request, username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            user.delete()
            return JsonResponse("User deleted.", safe=False)
        except:
            return JsonResponse("Cannot delete user because user does not exist.", safe=False)

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


# These are the functions for model Item
def get_item(request, item_id):
    if request.method == 'GET':
        try:
            item = Item.objects.get(pk=item_id)
            result = [item.as_json()]
            return JsonResponse(json.JSONDecoder().decode(json.dumps(result)), content_type="application/json", safe=False)
            #
            # return JsonResponse([{
            #         "item_id":item_id,
            #                 "name":item.name,
            #                  "price": item.price,
            #                  "date posted: ": item.datePosted,
            #                  "seller": str(item.seller),
            #                  }],
            #                 safe=False)

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
def update_item(request, username, item_id):
    if request.method == 'POST':
        try:
            item = Item.objects.get(pk=item_id)
            if (item.seller.username == username):
                item.price = request.POST.get('price')
                item.save()
                return JsonResponse("Item price updated.", safe=False)
            else:
                return JsonResponse("Item associated with user does not exist.", safe=False)

        except:
            return JsonResponse("Item not found.", safe=False)

def upload_item(request, username):

    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            authen = Authenticator.objects.get(user=user)
            logged_in = (authen.auth_num == request.POST.get('auth'))
            if logged_in:
                item = Item.objects.create(name=request.POST.get('name'),
                                           price=request.POST.get('price'),
                                           seller=user)
                item.save()
                return JsonResponse("Item successfully uploaded", safe=False)
            else:
                return JsonResponse('Cookie value does not match. Upload failed.', safe=False)
        except User.DoesNotExist:
            return JsonResponse("User does not exist. Upload failed.", safe=False)
        except Authenticator.DoesNotExist:
            return JsonResponse('User not logged in. Please login before uploading.', safe=False)
        except:
            return JsonResponse('Fields of item are incorrect. Upload failed.', safe=False)

def delete_item(request, username, item_id):

    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            item = Item.objects.get(pk=item_id)
            item.delete()
            return JsonResponse("Item successfully deleted", safe=False)
        except:
            return JsonResponse("User or Item does not exist. Delete failed.", safe=False)

def get_all_items(request):
    if request.method == "GET":
        try:
            itemsList = Item.objects.all()
            results = [ob.as_json() for ob in itemsList]
            return JsonResponse(json.JSONDecoder().decode(json.dumps(results)), content_type="application/json", safe=False)
        except:
            return JsonResponse("No items in database.", safe=False)

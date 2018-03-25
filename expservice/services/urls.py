from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^latestItems/', views.latestItems, name='latestItems'),
    url(r'^bakeryItem/(?P<pk>\d+)/', views.itemDetails, name='itemDetails'),
    url(r'^user/create/(?P<username>[-\w]+)/(?P<password>[-\w]+)/', views.createAccount, name='createAccount'),
    url(r'^user/logout/(?P<auth>\d+)/', views.logout, name='logout'),
    url(r'^user/login/(?P<username>[-\w]+)/(?P<password>[-\w]+)/', views.login, name='login'),
    url(r'^item/create/(?P<auth>\d+)/(?P<pk>\d+)/', views.create_new_item, name='create_new_item'),
]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^latestItems/', views.latestItems, name='latestItems'),
    url(r'^bakeryItem/(?P<pk>\d+)/', views.itemDetails, name='itemDetails'),
    url(r'^users/create$', views.createAccount, name='createAccount'),
    url(r'^users/logout', views.logout, name='logout'),
    url(r'^users/login$', views.login, name='login'),
    url(r'^users/uploadItem$', views.create_new_item, name='create_new_item'),
]

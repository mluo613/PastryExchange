from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bakeryItem/(?P<pk>\d+)$', views.bakeryItemDetails, name='bakeryItemDetails'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^createNewItem$', views.createNewItem, name='createNewItem'),
    url(r'^search$', views.search, name='search'),
    url(r'^deleteUser$', views.deleteUser, name='deleteUser'),
    url(r'^bakeryItem/update/(?P<pk>\d+)$', views.updateItem, name='updateItem'),
    url(r'^bakeryItem/delete/(?P<pk>\d+)$', views.deleteItem, name='deleteItem'),
]

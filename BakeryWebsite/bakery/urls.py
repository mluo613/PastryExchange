from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bakeryItem/(?P<pk>\d+)$', views.bakeryItemDetails, name='bakeryItemDetails'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^createNewItem$', views.createNewItem, name='createNewItem'),
]

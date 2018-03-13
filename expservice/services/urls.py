from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^latestItems/', views.latestItems, name='latestItems'),
    url(r'^bakeryItem/(?P<pk>\d+)/', views.itemDetails, name='itemDetails'),
]

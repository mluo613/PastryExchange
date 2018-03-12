from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
#    url(r'^bakeryItem/(?P<pk>\d+)$', views.bakeryItemDetailView.as_view(), name='bakeryItem-detail'),
]

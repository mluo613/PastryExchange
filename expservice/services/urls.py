from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^latestItems/', views.latestItems, name='latestItems'),
    url(r'^bakeryItem/(?P<pk>\d+)/', views.itemDetails, name='itemDetails'),
    url(r'^users/create$', views.createAccount, name='createAccount'),
    url(r'^users/logout', views.logout, name='logout'),
    url(r'^users/login$', views.login, name='login'),
    url(r'^users/uploadItem$', views.create_new_item, name='create_new_item'),
    url(r'^search/(?P<query>[\w\ ]+)/', views.search_items, name='search_items'),
    url(r'^items/updateItem/(?P<item_id>\d+)$', views.update_item, name='update_item'),
    url(r'^items/deleteItem/(?P<item_id>\d+)$', views.delete_item, name='delete_item'),
    url(r'^users/update', views.update_user, name='update_user'),
    url(r'^users/delete', views.delete_user, name='delete_user'),
]

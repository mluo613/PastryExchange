from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^users/uploadItem$', views.upload_item, name='upload_item'),

    url(r'^users/create$', views.create_user, name='create_user'),
    url(r'^users/login$', views.login, name='login'),
    url(r'^users/logout', views.logout, name='logout'),
    url(r'^users/update$', views.update_user, name='update_user'),
    url(r'^users/delete$', views.delete_user, name='delete_user'),
    url(r'^users/(?P<username>[-\w]+)$', views.get_user, name='get_user'),

    url(r'^items/(?P<item_id>\d+)/(?P<auth>[-\w]+)$', views.get_item, name='get_item'),
    url(r'^items/updateItem/(?P<item_id>\d+)$', views.update_item, name='update_item'),
    url(r'^items/deleteItem/(?P<item_id>\d+)$', views.delete_item, name='delete_item'),

    #    url(r'^items/(?P<item_name>[-\w]+)', views.getUpdate_item, name='getUpdate_item'),
    url(r'^getallitems$', views.get_all_items, name='get_all_items'),
    url(r'^getallusers$', views.get_all_users, name='get_all_users'),
    url(r'^getallloggedusers$', views.get_all_logged_users, name='get_all_logged_users'),

    url(r'^$', views.index, name='index'),
]

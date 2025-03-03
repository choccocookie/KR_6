from django.contrib import admin
from django.urls import path, include
from .views import index, read_clients, create_client, read_message, create_message, update_client, update_message, \
    create_mailing, read_mailing, update_mailing, delete_client
app_name='mailing'
urlpatterns = [

    path('read_client', read_clients, name='read_client'),
    path('create_client', create_client, name='create_clients'),
    path('<int:id_client>/update_client', update_client, name='update_client'),
    path('read_message', read_message, name='read_message'),
    path('create_message', create_message, name='create_message'),
    path('<int:id_message>/update_message', update_message, name='update_message'),
    path('<int:id_client>/delete_client', delete_client, name='delete_client')
]

urlpatterns += [
    path('create_mailing', create_mailing, name='create_mailing'),
    path('read_mailing', read_mailing, name='read_mailing'),
    path('<int:id_mailing>/update_mailing', update_mailing, name='update_mailing')
]
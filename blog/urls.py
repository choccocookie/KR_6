from django.urls import path
from .views import *
from .activate import activate

urlpatterns = [
    path('', home, name='home'),
    path('register', register, name='register'),
    path('sing_up', sing_up, name='sing_up'),
    path('logout', logout1, name='logout'),
    path('view-mailings', view_mailings, name='view_mailings'),
    path('view-user', view_users, name='view_users'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('close/<int:id_mailing>', close, name='close'),
    path('ban/<int:id_user>', ban, name='ban'),
    path('on_ban/<int:id_user>', on_ban, name='on_ban')

]
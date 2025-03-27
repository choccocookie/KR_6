from django.urls import path
from .views import register, sing_up, logout1, view_users, close, ban, on_ban, edit_user, user_profile
from .activate import activate

urlpatterns = [

    path('register/', register, name='register'),
    path('sing_up/', sing_up, name='sing_up'),
    path('logout/', logout1, name='logout'),
    path('view_user/', view_users, name='view_users'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('close/<int:id_mailing>/', close, name='close'),
    path('ban/<int:id_user>/', ban, name='ban'),
    path('on_ban/<int:id_user>/', on_ban, name='on_ban'),
    path('profile/', user_profile, name='profile')

]

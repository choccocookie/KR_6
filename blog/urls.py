from django.urls import path
from .views import home, view_mailings


urlpatterns = [
    path('', home, name='home'),
    path('view-mailings/', view_mailings, name='view_mailings'),


]

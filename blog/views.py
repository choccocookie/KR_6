from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from mailing.models import Mailing, Client

from .models import BlogPost
from django.views.decorators.cache import cache_page

# @cache_page(60*15)


def home(request):
    count_mailing = Mailing.objects.filter(AUTHOR_id=request.user.id).count()
    count_active_mailing = Mailing.objects.filter(
        AUTHOR_id=request.user.id, status='STARTED').count()
    unique_client = Client.objects.filter(author_id=request.user.id).count()
    random_blog_post = BlogPost.objects.order_by('?')[:3]

    context = {'message': 'Домашняя страница',
               'count_mailing': count_mailing,
               'count_active_mailing': count_active_mailing,
               'unique_client': unique_client,
               'random_blog_post': random_blog_post
               }
    return render(request, 'blog/home.html', context)


def view_mailings(request):
    if request.method == 'GET':
        all_mailings = Mailing.objects.all()
        print(all_mailings)
        return render(request, 'blog/interface_manager/view_mailings.html', {'mailings': all_mailings})

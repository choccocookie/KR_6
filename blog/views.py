from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from mailing.models import Mailing, CustomUser, Client
from .activate import send_activation_email
from .forms import CustomUserCreationForm
from .models import BlogPost
from django.views.decorators.cache import cache_page

#@cache_page(60*15)
def home(request):
    count_mailing = Mailing.objects.filter(AUTHOR_id=request.user.id).count()
    count_active_mailing = Mailing.objects.filter(AUTHOR_id=request.user.id, status='STARTED').count()
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

def view_users(request):
    if request.method == 'GET':
        get_users = CustomUser.objects.all()
        return render(request, 'blog/interface_manager/view_list_users.html', {'users': get_users})



def sing_up(request):
    if request.method == 'GET':
        return render(request, 'blog/sing_up.html', {'form': UserCreationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
        if user:
            login(request, user)
            return redirect('sing_up')
        else:
            return render(request, 'blog/sing_up.html', {'form': UserCreationForm,
                                                         'error': 'Такого пользователя нет'})

def logout1(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_activation_email(user, request)
            messages.success(request, 'Please check your email to activate your account.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/login.html', {'form': form})

def close(request, id_mailing):
    if request.method == 'POST':
        get_mailing_id = Mailing.objects.get(id=id_mailing)
        get_mailing_id.status = 'COMPLETED'
        get_mailing_id.save()
        return redirect('view_mailings')

def ban(request, id_user):
    if request.method == 'POST':
        get_user = CustomUser.objects.get(id=id_user)
        get_user.is_active = False
        get_user.save()
        return redirect('view_users')

def on_ban(request, id_user):
    if request.method == 'POST':
        get_user = CustomUser.objects.get(id=id_user)
        get_user.is_active = True
        get_user.save()
        return redirect('view_users')
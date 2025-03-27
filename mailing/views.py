from django.shortcuts import render, redirect
from pyexpat.errors import messages
from django.contrib import messages
from .forms import Client, ClientForm, Message, MessageForm, Mailing, MailingForm
from .models import Attempt



def index(request):
    client = Client.objects.all()
    print(client)
    context = {'message': 'Это домашняя страница'}

    return render(request, 'mailing/index.html', context)


def read_clients(request):
    client = Client.objects.all()
    print(client)
    context = {'message': 'Мы передали наш первый контекст в шаблон',
               'client': client}
    return render(request, 'mailing/CRUD_Clients/read_client.html', context)


def create_client(request):
    if request.method == 'GET':
        form = ClientForm()
        context = {'form': form}
        return render(request, 'mailing/CRUD_Clients/create_client.html', context)
    else:
        form = ClientForm(request.POST)
        if form.is_valid():
            new_client = form.save(commit=False)
            new_client.author = request.user
            new_client.save()

            return redirect('mailing:create_clients')
        else:
            return render(request, 'mailing/CRUD_Clients/create_client.html', {'error': 'Попробуйте еще раз'})


def read_message(request):

    message = Message.objects.filter(author=request.user.id)
    print(message)
    context = {'about': 'Мы передали контекст из read_message в шаблон read_message.html',
               'message': message}
    return render(request, 'mailing/CRUD_Message/read_message.html', context)


def create_message(request):
    form = MessageForm()

    context = {
        'form': form
    }

    if request.method == "GET":
        return render(request, 'mailing/CRUD_Message/create_message.html', context)

    else:
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.author = request.user
            new_message.save()
        return redirect('mailing:create_message')


def update_client(request, id_client):
    get_client = Client.objects.get(id=id_client)
    form = ClientForm(instance=get_client)
    if request.method == "GET":

        context = {
            "client": get_client,
            'up_form': form
        }
        return render(request, 'mailing/CRUD_Clients/update_client.html', context)
    else:
        up_form = ClientForm(request.POST, instance=get_client)
        if up_form.is_valid():
            up_form.save()
            return redirect('mailing:update_client', id_client)


def update_message(request, id_message):
    get_message = Message.objects.get(id=id_message)
    if request.method == "GET":

        context = {
            "message": get_message
        }
        return render(request, 'mailing/CRUD_Message/update_message.html', context)
    else:
        topic = request.POST.get('topic')
        content = request.POST.get('content')

        if topic and content:
            get_message.topic = topic
            get_message.content = content

            get_message.save()
            return redirect('update_message', id_message=id_message)
        else:
            return render(request, 'mailing/CRUD_Message/update_message.html',
                          {'error': 'Все поля должны быть заполнены', "message": get_message})


def create_mailing(request):

    form = MailingForm

    context = {
        "form": form
    }

    if request.method == 'GET':
        return render(request, 'mailing/CRUD_mailing/create_mailing.html', context)

    else:
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.AUTHOR = request.user
            mailing.save()
            mailing.clients.set(request.POST.getlist('clients'))
        return redirect('mailing:create_mailing')


def read_mailing(request):
    get_mailings = Mailing.objects.filter(AUTHOR=request.user.id)
    context = {
        'mailings': get_mailings
    }
    return render(request, 'mailing/CRUD_mailing/read_mailing.html', context)


def update_mailing(request, id_mailing):
    get_mailing = Mailing.objects.get(pk=id_mailing)
    if request.method == 'GET':

        context = {
            'up_form': MailingForm(instance=get_mailing)

        }

        return render(request, 'mailing/CRUD_Mailing/update_mailing.html', context)
    else:
        form = MailingForm(request.POST, instance=get_mailing)
        if form.is_valid():
            form.save()
            return redirect('mailing:update_mailing', id_mailing=id_mailing)


def delete_client(request, id_client):
    get_client = Client.objects.get(id=id_client)
    get_client.delete()
    messages.success(request, "Клиент успешно удален.")
    return redirect('mailing:read_client')


def delete_message(request, id_message):
    message = Message.objects.get(id=id_message)
    message.delete()
    messages.success(request, "Сообщение успешно удалено.")
    return redirect('mailing:read_message')


def delete_mailing(request, id_mailing):
    mailing = Mailing.objects.get(id=id_mailing)
    mailing.delete()
    messages.success(request, "Рассылочка успешно удалена.")
    return redirect('mailing:read_mailing')


def attempt_list(request):
    attempts = Attempt.objects.all()
    print(attempts)
    return render(request, 'mailing/attempt_list.html', {'attempts': attempts})

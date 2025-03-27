from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


def send_activation_email(user, request):
    subject = 'Activate your account'
    message = render_to_string('users/activate_email.html', {
        'user': user,
        'domain': request.get_host(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(subject, message, 'Trueinstrument.ru@yandex.ru', [user.email])


User = get_user_model()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        # Переход на страницу подтверждения
        return render(request, 'users/activate_completed.html')
    else:
        # Страница с ошибкой
        return render(request, 'users/activation_invalid.html')

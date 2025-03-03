from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


    def __str__(self):
        return self.email

class Config(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(validators=[MaxValueValidator(110)])
    descriptions = models.TextField()


    def __str__(self):
        return self.name


class Client(models.Model):
    email = models.EmailField(unique=True, blank=True)
    fullname = models.CharField(max_length=100, blank=True)
    comment = models.TextField(default='Нет коментариев')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.fullname} <{self.email}>'

class Message(models.Model):
    topic = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Тема {self.topic}, сообщение {self.content}'

class Mailing(models.Model):
    AUTHOR = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    CREATED = 'CREATED'

    INTERVAL_CHOICES = [
                        ('DAILY', 'Раз в день'),
                        ('WEEKLY', 'Раз в неделю'),
                        ('MONTHLY', 'Раз в месяц'),
    ]

    first_sanding_data = models.DateField()
    intervals = models.CharField(max_length=10, choices= INTERVAL_CHOICES)
    status = models.CharField(max_length=10, choices=
                                 [
                                    (STARTED, 'запущена' ),
                                     (COMPLETED, 'завершена'),
                                     (CREATED, 'создана'),
                                 ],
                                 default=CREATED)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f' {self.message}'




class Attempt(models.Model):
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, default=1)
    last_sanding_data = models.DateField()
    status = models.CharField(max_length=10, choices=
                                 [
                                    (FAILED, 'сбой'),
                                    (SUCCESS, 'успех'),
                                 ], null=True, blank=True
)
    server_answer = models.TextField(blank=True)

    def __str__(self):
        return f'Попытка отправки письма {self.mailing}, статус {self.status}'


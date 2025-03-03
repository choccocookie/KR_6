from django.contrib import admin
from .models import Config, Client, Mailing, Message, Attempt, CustomUser

# Register your models here.
admin.site.register(Config),
admin.site.register(Client),
admin.site.register(Mailing),
admin.site.register(Message),
admin.site.register(Attempt),
admin.site.register(CustomUser)
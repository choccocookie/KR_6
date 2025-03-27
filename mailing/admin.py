from django.contrib import admin
from .models import Client, Mailing, Message, Attempt

# Register your models here.

admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(Attempt)

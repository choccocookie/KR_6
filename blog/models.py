from django.db import models

from mailing.models import CustomUser


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    count_view = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

# Create your models here.

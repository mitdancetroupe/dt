import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='posts')
    body = models.TextField()
    created = models.DateTimeField(default=datetime.datetime.now)


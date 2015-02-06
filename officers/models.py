import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Officer(models.Model):
    user = models.ForeignKey(User, related_name='user')
    position = models.CharField(max_length = 30)
    order = models.IntegerField()
    def __unicode__(self):
        return self.position

import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Officer(models.Model):
    user = models.ForeignKey(User, related_name='user')
    order = models.IntegerField()
    photo = models.ImageField(upload_to=settings.DANCER_IMAGE_DIR, blank=True)

    def __unicode__(self):
        return self.position

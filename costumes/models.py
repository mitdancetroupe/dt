from django.db import models
from django.conf import settings

from dt.dances.models import Dance

# Create your models here.
class Costume(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=30)
    location = models.CharField(max_length=20)
    photo = models.ImageField(upload_to=settings.COSTUME_IMAGE_DIR, blank=True)
    dances = models.ManyToManyField(Dance, blank=True, related_name='costumes')


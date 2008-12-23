from django.db import models

from django.contrib.auth.models import User
from dt.shows.models import *

# Create your models here.
class Dance(models.Model):
    LEVEL_CHOICES = (
        (0, 'All'),
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced')
    )
    name = models.CharField(max_length = 255)
    style = models.CharField(max_length = 255)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    description = models.TextField(blank=True)
    choreographers = models.ManyToManyField(User, blank=True,
                                            related_name='choreographed')
    dancers = models.ManyToManyField(User, blank=True, related_name='danced_in')
    show = models.ForeignKey(Show, related_name='dances')
    def __str__(self):
        return self.name
    class Admin:
        list_display = ('name', 'show', 'style', 'level')


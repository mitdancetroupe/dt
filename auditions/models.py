from django.db import models
from dt import core

# Create your models here.
class PrefSheet(models.Model):
    user = models.ForeignKey(core.models.User)
    show = models.ForeignKey(core.models.Show)
    conflicts = models.TextField()

class Pref(models.Model):
    prefsheet = models.ForeignKey('PrefSheet', related_name='prefs')
    dance = models.ForeignKey(core.models.Dance)
    pref = models.PositiveSmallIntegerField()
    class Meta:
        ordering = ['-pref']
        unique_together = (('dance', 'pref'),)


from django.db import models
from django.conf import settings
from django.contrib import auth
from dt import core

# Create your models here.
class PrefSheet(models.Model):
    user = models.ForeignKey(auth.models.User, related_name='prefsheets')
    conflicts = models.TextField(blank=True)
    desired_dances = models.PositiveSmallIntegerField()
    show = models.ForeignKey(core.models.Show)
    def __str__(self):
        return "%s / %s" % (self.user, self.show)
    class Meta:
        unique_together = (('user', 'show',),)

class Pref(models.Model):
    prefsheet = models.ForeignKey(PrefSheet, related_name='prefs')
    dance = models.ForeignKey(core.models.Dance, core=True)
    pref = models.PositiveSmallIntegerField(core=True)
    def __str__(self):
        return "%s: %s" % (self.dance, self.pref)
    class Meta:
        ordering = ('prefsheet', '-pref')
        unique_together = (('prefsheet', 'dance'), ('prefsheet', 'pref'),)

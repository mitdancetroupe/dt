from django.db import models
from django.conf import settings
from django.contrib import auth
from dt import core

class PrefSheetManager(models.Manager):
    def assign_numbers(self, show):
        prefsheets = self.filter(show=show).order_by('?')
        n = prefsheets.count()
        for i, prefsheet in zip(range(1,n+1), prefsheets):
            prefsheet.audition_number = i
            prefsheet.save()

class PrefSheet(models.Model):
    audition_number = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(auth.models.User, related_name='prefsheets')
    conflicts = models.TextField(blank=True)
    desired_dances = models.PositiveSmallIntegerField()
    show = models.ForeignKey(core.models.Show)
    objects = PrefSheetManager()
    def __str__(self):
        return "%s / %s" % (self.user, self.show)
    class Meta:
        unique_together = (('user', 'show',), ('audition_number', 'show'),)
        permissions = (('can_list', 'Can list prefsheets'),)


class Pref(models.Model):
    prefsheet = models.ForeignKey(PrefSheet, related_name='prefs')
    dance = models.ForeignKey(core.models.Dance, related_name='prefs')
    pref = models.PositiveSmallIntegerField()
    def __str__(self):
        return "%s: %s" % (self.dance, self.pref)
    class Meta:
        ordering = ('prefsheet', 'pref')
        unique_together = (('prefsheet', 'dance'), ('prefsheet', 'pref'),)

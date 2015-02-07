from django.db import models
from django.conf import settings
from django.contrib import auth
from dt import shows

class PrefSheetManager(models.Manager):
    def assign_numbers(self, show):
        prefsheets = self.filter(show=show).order_by('?')
        n = prefsheets.count()
        for prefsheet in prefsheets:
            prefsheet.audition_number = None
            prefsheet.save()
        for i, prefsheet in zip(range(1,n+1), prefsheets):
            prefsheet.audition_number = i
            prefsheet.save()

class PrefSheet(models.Model):
    audition_number = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(auth.models.User, related_name='prefsheets')
    availability = models.TextField(blank=True, help_text='')
    conflicts = models.TextField(blank=True, help_text='For each conflict checked above, please list the time and reason (i.e. Sundays 7-9pm Fraternity Chapter Meeting).')
    desired_dances = models.PositiveSmallIntegerField()
    show = models.ForeignKey(shows.models.Show)
    accepted_dances = models.PositiveSmallIntegerField(default=0)
    rejected_dances = models.PositiveSmallIntegerField(default=0)
    objects = PrefSheetManager()
    def __unicode__(self):
        return u"%s / %s" % (self.user, self.show)
    class Meta:
        ordering = ('audition_number',)
        unique_together = (('user', 'show',), ('audition_number', 'show'),)
        permissions = (('can_list', 'Can list prefsheets'),)


class Pref(models.Model):
    prefsheet = models.ForeignKey(PrefSheet, related_name='prefs')
    dance = models.ForeignKey(shows.models.Dance, related_name='prefs')
    pref = models.PositiveSmallIntegerField()
    accepted = models.NullBooleanField()
    return_if_not_placed = models.BooleanField(default=False)
    def __unicode__(self):
        return u"%s: %s" % (self.dance, self.pref)
    class Meta:
        ordering = ('prefsheet', 'pref')
        unique_together = (('prefsheet', 'dance'), ('prefsheet', 'pref'),)

class Availability(models.Model):
    DAY_CHOICES = (
        ('u', 'Sunday'),
        ('m', 'Monday'),
        ('t', 'Tuesday'),
        ('w', 'Wednesday'),
        ('r', 'Thursday'),
        ('f', 'Friday'),
        ('s', 'Saturday'))

    day = models.CharField(max_length=1, choices=DAY_CHOICES)
    prefsheet = models.ForeignKey(PrefSheet, related_name='availabilities', default=0)
    hour = models.CharField(max_length = 12)
    available = models.BooleanField(default=True)
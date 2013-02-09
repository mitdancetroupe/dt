from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class ShowManager(models.Manager):
    def get_by_semester(self, semester, year):
        """
        Returns a show based on a semester and year, for example: 'S' and 08
        for the spring 2008 show.
        """
        try:
            year = int(year)
            semester = {'S': 0, 'F': 1}[semester]
            year = 1900 + year if year >= 90 else 2000 + year
            show = self.get(year=year, semester=semester)
            return show
        except KeyError:
            raise Show.DoesNotExist

class Show(models.Model):
    SEMESTER_CHOICES = ((0, 'Spring'), (1, 'Fall'))
    name = models.CharField(max_length = 255)
    year = models.IntegerField()
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    info = models.TextField()
    slug = models.SlugField()
    objects = ShowManager()
    prefsheets_open = models.BooleanField(help_text = "Whether preferences sheets are being accepted for this show. Disabling will (re)generate audition numbers.")
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('dt.shows.views.show_detail', args = [str(self.slug)])
    class Meta:
        ordering = ('-year', '-semester')


class Dance(models.Model):
    LEVEL_CHOICES = (
        (0, 'All'),
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Intermediate/Advanced'),
        (5, 'Beginner/Intermediate')
    )
    name = models.CharField(max_length = 255)
    style = models.CharField(max_length = 255)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    description = models.TextField(blank=True)
    choreographers = models.ManyToManyField(User, blank=True,
                                            related_name='choreographed')
    dancers = models.ManyToManyField(User, blank=True, related_name='danced_in')
    show = models.ForeignKey(Show, related_name='dances')
    def __unicode__(self):
        return self.name
    class Admin:
        list_display = ('name', 'show', 'style', 'level')

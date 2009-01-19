from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

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
    objects = ShowManager()
    def __str__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('dt.shows.views.show_detail', [str(self.id)])
    class Meta:
        ordering = ('-year', '-semester')


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


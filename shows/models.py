from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

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
    show = models.ForeignKey('Show', related_name='dances')
    def __str__(self):
        return self.name
    class Admin:
        list_display = ('name', 'show', 'style', 'level')

class Show(models.Model):
    SEMESTER_CHOICES = ((0, 'Spring'), (1, 'Fall'))
    name = models.CharField(max_length = 255)
    year = models.IntegerField()
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ('-year', '-semester')


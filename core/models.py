from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Dancer(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    first_name = models.CharField(maxlength=30)
    last_name = models.CharField(maxlength=30)
    gender = models.CharField(maxlength=1, choices=GENDER_CHOICES, core=True)
    email = models.EmailField()
    year = models.IntegerField(null=True, blank=True)
    living_group = models.CharField(maxlength=30, blank=True)
    experience = models.TextField(blank=True)
    photo = models.ImageField(upload_to=settings.DANCER_IMAGE_DIR, blank=True)
    def __str__(self):
        return self.first_name + " " + self.last_name
    class Admin:
        list_display = ('email', 'first_name', 'last_name', 'year',)
    class Meta:
        unique_together = (('email',),)

class Dance(models.Model):
    LEVEL_CHOICES = (
        (0, 'All'),
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced')
    )
    name = models.CharField(maxlength = 255)
    style = models.CharField(maxlength = 255)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    description = models.TextField(blank=True)
    choreographers = models.ManyToManyField(Dancer, 
                                            related_name='choreographed')
    dancers = models.ManyToManyField(Dancer, related_name='danced_in')
    show = models.ForeignKey('Show', related_name='dances')
    def __str__(self):
        return self.name
    class Admin:
        list_display = ('name', 'show', 'style', 'level')

class Show(models.Model):
    SEMESTER_CHOICES = ((0, 'Spring'), (1, 'Fall'))
    name = models.CharField(maxlength = 255)
    year = models.IntegerField()
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    def __str__(self):
        return self.name
    class Admin:
        list_display = ('name', 'semester', 'year')


from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    GENDER_CHOICES = ((0, 'Male'), (1, 'Female'))
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, core=True)
    year = models.IntegerField(null=True, blank=True)
    living_group = models.CharField(maxlength=30, blank=True)
    experience = models.TextField(blank=True)
    photo = models.ImageField(upload_to=settings.PROFILE_IMAGE_DIR, 
                              blank=True)
    user = models.ForeignKey(User, unique=True, edit_inline=models.STACKED,
                                   num_in_admin=1, max_num_in_admin=1,
                                   min_num_in_admin=1, num_extra_on_change=0)
    def __str__(self):
        return self.user.username

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
    description = models.TextField()
    choreographers = models.ManyToManyField(User, 
                                            related_name='choreographed')
    dancers = models.ManyToManyField(User, related_name='danced_in')
    show = models.ForeignKey('Show', related_name='dances')
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


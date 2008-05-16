from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    GENDER_CHOICES = ((0, 'Male'), (1, 'Female'))
    year = models.IntegerField(core=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, core=True)
    user = models.ForeignKey(User, unique=True, edit_inline=models.STACKED,
                                   num_in_admin=1, max_num_in_admin=1,
                                   min_num_in_admin=1, num_extra_on_change=0)
    def __str__(self):
        return self.user.username
    class Admin:
        pass

class Dance(models.Model):
    LEVEL_CHOICES = (
        (0, 'All'),
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced')
    )
    name = models.CharField(maxlength = 255)
    description = models.TextField()
    style = models.CharField(maxlength = 255)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    choreographers = models.ManyToManyField(User, 
                                            related_name='choreographed')
    dancers = models.ManyToManyField(User, related_name='danced_in')
    show = models.ForeignKey('Show')
    class Admin:
        pass

class Show(models.Model):
    SEMESTER_CHOICES = ((0, 'Spring'), (1, 'Fall'))
    name = models.CharField(maxlength = 255)
    year = models.IntegerField()
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    def __str__(self):
        return self.name
    class Admin:
        list_display = ('name', 'semester', 'year')


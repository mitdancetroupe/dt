from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    AFFILIATION_CHOICES = (('U', 'Undergraduate'), ('G', 'Graduate'),
                           ('O', 'Other'), ('N', 'Non-MIT'))
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    year = models.IntegerField(null=True, blank=True)
    affiliation = models.CharField(max_length=1, choices=AFFILIATION_CHOICES)
    living_group = models.CharField(max_length=30, blank=True)
    experience = models.TextField(blank=True)
    phone_number = models.PhoneNumberField(blank=True)
    def photo_path(instance, filename):
        return "%s/%s-%s" % (settings.DANCER_IMAGE_DIR, instance.user.username,
                             filename)
    photo = models.ImageField(upload_to=photo_path, blank=True)
    def __str__(self):
        return "Profile for %s" % self.user

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
    choreographers = models.ManyToManyField(User, 
                                            related_name='choreographed')
    dancers = models.ManyToManyField(User, related_name='danced_in')
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


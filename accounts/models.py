from django.conf import settings
from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('N', 'Prefer Not to Answer'))
    AFFILIATION_CHOICES = (('U', 'Undergraduate'), ('G', 'Graduate'),
                           ('O', 'Other'), ('N', 'Non-MIT'))
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    year = models.IntegerField(null=True, blank=True)
    affiliation = models.CharField(max_length=1, choices=AFFILIATION_CHOICES)
    living_group = models.CharField(max_length=30, blank=True)
    experience = models.TextField(blank=True)
    phone_number = PhoneNumberField(blank=True, help_text='An optional phone number we can use to reach you if necessary.')
    photo = models.ImageField(upload_to=settings.DANCER_IMAGE_DIR, blank=True, help_text='An optional photo of yourself.')

    ordering = ('username',)
    def __unicode__(self):
        return u"Profile for %s" % self.user
    def save(self, height=300, width=200):
        super(UserProfile, self).save()
        if self.photo:
            filename = self.photo.path
            image = Image.open(filename)
            image.thumbnail((width, height), Image.ANTIALIAS)
            image.save(filename)

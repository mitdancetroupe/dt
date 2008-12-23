from django.conf import settings
from django.db import models

class Show(models.Model):
    SEMESTER_CHOICES = ((0, 'Spring'), (1, 'Fall'))
    name = models.CharField(max_length = 255)
    year = models.IntegerField()
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ('-year', '-semester')


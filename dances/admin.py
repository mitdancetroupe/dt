from django.contrib import admin
from dt.dances.models import *

class DanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'style', 'level')

admin.site.register(Dance, DanceAdmin)



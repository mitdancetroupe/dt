from django.contrib import admin
from dt.shows.models import *

class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'semester')

admin.site.register(Show, ShowAdmin)


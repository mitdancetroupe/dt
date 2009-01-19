from django.contrib import admin
from dt.shows.models import *

class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'semester')

class DanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'style', 'level')


admin.site.register(Show, ShowAdmin)
admin.site.register(Dance, DanceAdmin)


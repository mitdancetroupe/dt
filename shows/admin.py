from django.contrib import admin
from dt.shows.models import *

class DanceInline(admin.TabularInline):
    model = Dance
    exclude = ('dancers',)

class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'semester')
    inlines = (DanceInline,)

class DanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'style', 'level')
    filter_horizontal = ('choreographers', 'dancers')

admin.site.register(Show, ShowAdmin)
admin.site.register(Dance, DanceAdmin)


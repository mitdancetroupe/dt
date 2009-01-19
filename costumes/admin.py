from django.contrib import admin
from dt.costumes.models import *


class CostumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'color', 'quantity',)
    search_fields = ('name', 'location', 'color',)
    list_filter = ('location', 'color',)

admin.site.register(Costume, CostumeAdmin)

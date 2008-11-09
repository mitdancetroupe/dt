from django.contrib import admin
from dt.costumes.models import *


class CostumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'quantity',)

admin.site.register(Costume, CostumeAdmin)

from django.db import models
from django.contrib import admin
from dt.costumes.models import *
from dt.widgets import AdminImageWidget


class CostumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'color', 'quantity',)
    search_fields = ('name', 'location', 'color',)
    list_filter = ('location', 'color',)
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }

admin.site.register(Costume, CostumeAdmin)

from django.contrib import admin
from dt.auditions.models import *

from django.contrib import auth

class PrefInline(admin.TabularInline):
    model = Pref

class PrefSheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'audition_number', 'show')
    list_filter = ('show',)
    inlines = [ PrefInline ]


admin.site.register(PrefSheet, PrefSheetAdmin) 

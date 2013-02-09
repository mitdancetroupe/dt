from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from dt.auditions.models import *

from django.contrib import auth

class PrefInline(admin.TabularInline):
    model = Pref

class PrefSheetAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.order_by('username'))
    class Meta:
        model = PrefSheet

class PrefSheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'audition_number', 'show')
    list_filter = ('show',)
    inlines = [ PrefInline ]
    form = PrefSheetAdminForm
    search_fields = ('user__username',)


admin.site.register(PrefSheet, PrefSheetAdmin) 

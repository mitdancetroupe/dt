from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from tinymce.widgets import TinyMCE

class TinyMCEFlatpageForm(FlatpageForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 60}))

class TinyMCEFlatPageAdmin(FlatPageAdmin):
    form = TinyMCEFlatpageForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)

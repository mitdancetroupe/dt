from django.contrib import admin
from dt.officers.models import *
from officers.forms import *

class OfficerAdmin(admin.ModelAdmin):
    list_display = ('position', 'order', 'user')

    list_editable = ('order',)
    field_options = {'fields': ('position', 'order', 'user')}
    form = OfficerForm

admin.site.register(Officer, OfficerAdmin)
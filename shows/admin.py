from django.contrib import admin
from dt.shows.models import *
from dt.auditions.models import PrefSheet
from shows.forms import ShowForm

class DanceInline(admin.TabularInline):
    model = Dance
    exclude = ('dancers', 'choreographers')

class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'semester', 'prefsheets_open')
    inlines = (DanceInline,)
    form = ShowForm

    def save_model(self, request, obj, form, change):
        if 'prefsheets_open' in form.changed_data and not obj.prefsheets_open:
            PrefSheet.objects.assign_numbers(obj)
        super(ShowAdmin, self).save_model(request, obj, form, change)

class DanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'style', 'level')
    filter_horizontal = ('choreographers', 'dancers')

admin.site.register(Show, ShowAdmin)
admin.site.register(Dance, DanceAdmin)


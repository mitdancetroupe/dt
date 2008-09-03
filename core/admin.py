from django.contrib import admin
from dt.core.models import *

from django.contrib import auth

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1
    max_num = 1

class UserAdmin(auth.admin.UserAdmin):
    inlines = [ UserProfileInline ]

class ShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'semester')

class DanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'style', 'level')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Show, ShowAdmin)
admin.site.register(Dance, DanceAdmin) 

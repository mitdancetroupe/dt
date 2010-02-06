from django.contrib import admin
from django.db import models
from dt.accounts.models import *
from dt.widgets import AdminImageWidget

from django.contrib import auth

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1
    max_num = 1
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }

class UserAdmin(auth.admin.UserAdmin):
    inlines = [ UserProfileInline ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


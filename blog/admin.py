from django.contrib import admin
from dt.blog.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title',)
    field_options = {'fields': ('title', 'body', 'author', 'created',)}

admin.site.register(Post, PostAdmin)

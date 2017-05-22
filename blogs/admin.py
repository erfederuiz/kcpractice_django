from __future__ import unicode_literals

from django.contrib import admin

from blogs.models import Category, Blog, Post

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Blog)

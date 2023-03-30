from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import (User, Review, Comment, Title,
                     Category, Genre)


class Admin(UserAdmin):
    ...


admin.site.register(User, Admin)
admin.site.unregister(Group)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)

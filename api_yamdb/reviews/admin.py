from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User


class Admin(UserAdmin):
    ...


admin.site.register(User, Admin)
admin.site.unregister(Group)

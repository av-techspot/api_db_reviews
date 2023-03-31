from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Category, Comment, Genre, Review, Title, TitleGenre, User


class Admin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Дополнительно'), {'fields': ('bio', 'role')}),
    )
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'role')
    list_editable = ('is_staff', 'role',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score', 'pub_date',)
    search_fields = ('title', 'author',)
    list_filter = ('author', 'score',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category',)
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year', 'category',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date', )
    search_fields = ('review',)
    list_filter = ('author',)


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre',)
    list_editable = ('genre',)
    search_fields = ('title',)
    list_filter = ('genre',)


admin.site.register(User, Admin)
admin.site.unregister(Group)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Category, Comment, Genre, Review, Title, TitleGenre, User

admin.site.unregister(Group)


@admin.register(User)
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
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'role',
    )
    list_editable = ('is_staff', 'role', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score', 'pub_date', )
    search_fields = ('title', 'author', )
    list_filter = ('author', 'score', )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'year', 'description', 'category', 'average_rating', )
    list_editable = ('category', )
    search_fields = ('name', )
    list_filter = ('year', 'category', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date', )
    search_fields = ('review', )
    list_filter = ('author', )


@admin.register(TitleGenre)
class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', )
    list_editable = ('genre', )
    search_fields = ('title', )
    list_filter = ('genre', )

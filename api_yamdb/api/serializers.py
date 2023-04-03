from datetime import date

from rest_framework import serializers
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User


class UserOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User
        read_only_fields = ('role', )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', )
        model = User

    def validate_username(self, value: str) -> str:
        if value == 'me':
            raise serializers.ValidationError(
                f'{value} не корректное имя пользователя'
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id', 'text', 'author', 'score', 'pub_date',
        )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', )
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGETSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='average_rating', read_only=True,
    )
    category = CategorySerializer(read_only=True, )
    genre = GenreSerializer(many=True, read_only=True, )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'category', 'genre',
        )
        model = Title


class TitlePOSTSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='average_rating', read_only=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        read_only=False,
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        read_only=False,
        many=True,
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'category', 'genre',
        )
        model = Title

    def validate_year(self, value):
        year = date.today().year
        if value > year or year <= 0:
            raise serializers.ValidationError(
                'Некорректное значение года'
            )
        return value

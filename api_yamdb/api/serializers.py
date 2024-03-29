from datetime import date

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return {'name': obj.name,
                'slug': obj.slug}


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
        fields = (
            'name', 'slug'
        )
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        exclude = ('title', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'slug'
        )
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='average_rating', read_only=True,
    )
    category = CustomSlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        read_only=False,
    )
    genre = CustomSlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        read_only=False,
        many=True,
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = date.today().year
        if value > year or year <= 0:
            raise serializers.ValidationError(
                'Некорректное значение года'
            )
        return value

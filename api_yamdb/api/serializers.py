from django.core.exceptions import ObjectDoesNotExist
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
        read_only_fields = ('role',)


class RegistrationDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email',)
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(f'{value} isn\'t valid username')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title', 'text', 'author', 'score', 'pub_date',
        )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'text', 'author', 'pub_date',
        )
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.Serializer):
    name = serializers.CharField(
        label='Название', required=True, max_length=256
    )
    year = serializers.IntegerField(label='Год', required=True)
    rating = serializers.IntegerField(source='average_rating', read_only=True)
    description = serializers.CharField(label='Описание', required=False)
    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=True)

    def validate(self, data):
        pass

    def create(self, validated_data):
        slug_category = validated_data.pop('category')
        slug_genre = validated_data.pop('genre')
        try:
            category = Category.objects.get(slug=slug_category)
            genre = Genre.objects.get(slug=slug_genre)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                f'Either the "{slug_category}" or the "{slug_genre}" doesn\'t'
                ' exist.'
            )

        title = Title.objects.create(category=category, **validated_data)
        TitleGenre.objects.create(title=title, genre=genre)
        return title

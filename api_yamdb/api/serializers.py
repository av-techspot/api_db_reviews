from rest_framework.serializers import ModelSerializer
from reviews.models import Category, Comment, Genre, Review, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class ReviewSerializer(ModelSerializer):
    class Meta:
        fields = (
            'title', 'text', 'author', 'score', 'pub_date',
        )
        model = Review


class CommentSerializer(ModelSerializer):
    class Meta:
        fields = (
            'review', 'text', 'author', 'pub_date',
        )
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre

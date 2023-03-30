from rest_framework.serializers import ModelSerializer
from reviews.models import Comment, Review, User


class UserSerializer(ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User


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

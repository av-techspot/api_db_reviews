from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reviews.models import Comment, Review, User

#from .exceptions import UserExist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User


class RegistrationDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email',)
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(f'{value} isn\'t valid username')
#        if (User.objects.filter(username=value)):
#            raise UserExist('Такой пользователь уже зарегистрирован.')
        return value

#    def validate(self, data):
#        if (
#            data.get('username')
#            and User.objects.filter(username=data.get('username'))
#        ):
#            raise UserExist('Такой пользователь уже зарегистрирован.')
#        return data


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

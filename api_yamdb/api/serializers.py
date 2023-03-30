from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import User

from .exceptions import UserExist


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
        if (User.objects.filter(username=value)):
            raise UserExist('Такой пользователь уже зарегистрирован.')
        return value

    def validate(self, data):
        if (
            data.get('username')
            and User.objects.filter(username=data.get('username'))
        ):
            raise UserExist('Такой пользователь уже зарегистрирован.')
        return data

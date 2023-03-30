from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import get_error_detail
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User

from .exceptions import UserExist
from .serializers import RegistrationDataSerializer, UserSerializer


@api_view(['POST'])
def registration(request):
    serializer = RegistrationDataSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except UserExist:
        return Response({}, status=status.HTTP_200_OK)
    except exceptions.ValidationError:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username'),
        )
        #user.email_user(
        #    subject="Подтвердите регистрацию",
        #    message="confirmation_code: "
        #            f"{default_token_generator.make_token(user)}",
        #    from_email='a@a.ru',
        #)
        return Response({}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    if (
        not request.data
        or not request.data.get('username')
    ):
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=request.data.get('username'))
    if default_token_generator.check_token(
        user,
        request.data.get('confirmation_code')
    ):
        return Response(
            {'token': f'{AccessToken.for_user(user)}'},
            status=status.HTTP_200_OK
        )
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

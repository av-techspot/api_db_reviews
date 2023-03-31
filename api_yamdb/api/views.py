from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, User

from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          RegistrationDataSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = RegistrationDataSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except exceptions.ValidationError as e:
        if (
            e.get_codes().get('username') == ['unique']
            and get_object_or_404(
                User,
                username=request.data.get('username')
            ).email == request.data.get('email')
        ):
            user = get_object_or_404(
                User,
                username=request.data.get('username'),
            )
            user.email_user(
                subject="Подтвердите регистрацию",
                message="confirmation_code: "
                        f"{default_token_generator.make_token(user)}",
                from_email='a@a.ru',
            )
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username'),
        )
        user.email_user(
            subject="Подтвердите регистрацию",
            message="confirmation_code: "
                    f"{default_token_generator.make_token(user)}",
            from_email='a@a.ru',
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
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
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = [IsAdminOrReadOnly]

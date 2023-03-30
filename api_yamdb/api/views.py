from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
from rest_framework import status

from reviews.models import Category, Genre, User

from .serializers import UserSerializer, CategorySerializer, GenreSerializer
from .permissions import IsAdminOrReadOnly


def registration(request):
    ...


def get_token(request):
    ...


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
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
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = [IsAdminOrReadOnly]

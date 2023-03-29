from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from reviews.models import User

from .serializers import UserSerializer


def registration(request):
    ...


def get_token(request):
    ...


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

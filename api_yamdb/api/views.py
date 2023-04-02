from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationDataSerializer,
                          ReviewSerializer, TitleGETSerializer,
                          TitlePOSTSerializer, UserOwnerProfileSerializer,
                          UserSerializer)


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete',)
    permission_classes = (IsAdmin,)

    @action(
        methods=('get', 'patch',), detail=False, url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserOwnerProfileSerializer,
    )
    def get_or_update_owner_profile(self, request):
        if request.method == 'GET':
            return Response(
                self.get_serializer(
                    request.user).data, status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().select_related('category').prefetch_related(
        'genre')
    serializer_class = TitleGETSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleGETSerializer
        else:
            return TitlePOSTSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (get_token, registration, CategoryViewSet, GenreViewSet,
                    TitleViewSet, UserViewSet)

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_token, name='get_token'),
]

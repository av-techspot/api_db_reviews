from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (get_token, registration, UserViewSet, CategoryViewSet)

router = SimpleRouter()
router.register('users', UserViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_token, name='get_token'),
]

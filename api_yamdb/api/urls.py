from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, get_token, registration

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registration, name='registration'),
    path('v1/auth/token/', get_token, name='get_token'),
]

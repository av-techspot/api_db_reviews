from rest_framework.permissions import SAFE_METHODS, BasePermission
from reviews.constants import UserRoles


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == UserRoles.ADMIN
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == UserRoles.ADMIN
            )
        )

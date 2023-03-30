from rest_framework.permissions import BasePermission, SAFE_METHODS
from reviews.constants import UserRoles


class IsAdminOrReadOnly(BasePermission):
    # def has_permission(self, request, view):
    #     return bool(
    #         request.method in SAFE_METHODS
    #         or request.user.is_authenticated
    #         and request.user.role == UserRoles.ADMIN
    #     )
    pass

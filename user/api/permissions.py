from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAuthenticatedAndVerified(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied("User is not Authenticated")

        # if not user.is_verified:
        #     raise PermissionDenied("User is not Verified")

        return True

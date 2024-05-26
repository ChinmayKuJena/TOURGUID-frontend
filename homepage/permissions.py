from rest_framework.permissions import BasePermission

class IsAuthenticatedOrTokenHasPermission(BasePermission):
    """
    Custom permission to allow access if the user is authenticated or has a valid token.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_authenticated or request.auth)

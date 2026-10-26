from rest_framework.permissions import BasePermission


class IsAdminOrAdvocateUser(BasePermission):
    # Placeholder for role rules: tighten when roles are finalised.
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

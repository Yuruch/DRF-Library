from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only administrators to edit or delete resources.

    - SAFE_METHODS (e.g., GET, HEAD, OPTIONS) are allowed for any authenticated user.
    - Non-safe methods (e.g., POST, PUT, DELETE) are restricted to users with admin privileges (is_staff=True).
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
            )
            or (request.user and request.user.is_staff)
        )

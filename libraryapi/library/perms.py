from rest_framework import permissions

class IsVerifiedLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'LIBRARIAN'
            and request.user.is_verified_librarian
        )
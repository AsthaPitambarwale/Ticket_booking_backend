from rest_framework import permissions

class IsBookingOwner(permissions.BasePermission):
    """Permission to allow only booking owner to cancel the booking."""

    def has_object_permission(self, request, view, obj):
        # obj is Booking instance
        return obj.user == request.user

from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj,
            role=BoardParticipant.Role.owner
        ).exists()

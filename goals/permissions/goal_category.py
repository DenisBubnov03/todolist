from rest_framework import permissions

from goals.models import BoardParticipant


class GoalCategoryPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()

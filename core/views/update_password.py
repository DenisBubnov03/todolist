from rest_framework import permissions
from rest_framework.generics import UpdateAPIView

from core.serializers import UpdatePasswordSerializer


class UpdatePasswordView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user
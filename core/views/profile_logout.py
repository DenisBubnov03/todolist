from django.contrib.auth import logout
from rest_framework import (
    permissions,
    status
)
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from core.models import User
from core.serializers import ProfileSerializer


class ProfileView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
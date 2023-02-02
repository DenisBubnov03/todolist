from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import CreateUserSerializer


class RegistrationView(CreateAPIView):
    model = User
    serializer_class = CreateUserSerializer
from django.contrib.auth import authenticate
from rest_framework import (
    exceptions,
    serializers
)

from core.models import User


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )
        if not user:
            raise exceptions.AuthenticationFailed('Имя пользователя или пароль некорректны')

        return user
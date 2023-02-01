from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import (
    exceptions,
    serializers
)

from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat',
        )

    def create(self, validated_data):
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password_repeat', None)

        if password != password_repeat:
            raise exceptions.ValidationError('Пароли не совпадают')

        validated_data['password'] = make_password(password)

        user = super().create(validated_data)
        return user
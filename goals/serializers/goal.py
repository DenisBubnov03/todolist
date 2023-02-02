from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import Goal


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('Не разрешено в удаленной категории')

        if value.user != self.context['request'].user:
            raise serializers.ValidationError('Не являетесь владельцем категории')

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('Не являетесь владельцем категории')

        return value

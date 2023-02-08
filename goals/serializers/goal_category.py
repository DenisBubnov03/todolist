from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import GoalCategory, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_board(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('нет доступа к удалённым данным')
        if not BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user
        ).exists():
            raise serializers.ValidationError('создавать могут только владелец и редакторы')
        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

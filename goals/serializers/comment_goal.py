from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models import GoalComment, BoardParticipant


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_goal(self, value):
        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context["request"].user
        ).exists():
            raise serializers.ValidationError('создавать могут только владелец и редакторы')
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')
        fields = '__all__'

    def validate_goal(self, value):
        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user=self.context["request"].user
        ).exists():
            raise serializers.ValidationError('изменения могут вносить только владелец и редакторы')
        return value

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalComment, Goal
from goals.permissions import CommentPermissions
from goals.serializers import CommentSerializer, CommentCreateSerializer


class CommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        ).exclude(goal__status=Goal.Status.archived)


class CommentListView(ListAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        ).exclude(goal__status=Goal.Status.archived)

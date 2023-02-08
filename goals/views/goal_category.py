from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalCategory, Goal
from goals.permissions import GoalCategoryPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        Goal.objects.filter(
            category_id__exact=instance.id
        ).update(status=Goal.Status.archived)
        instance.save()
        return instance


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = [
        'title',
        'created',
    ]
    ordering = ['title']
    search_fields = ['title']
    filterset_fields = [
        'board',
        'user'
    ]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )

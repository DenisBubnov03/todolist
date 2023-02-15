import factory
from django.utils import timezone


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'core.User'

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class BoardFactory(DatesFactoryMixin):
    class Meta:
        model = 'goals.Board'

    title = factory.Faker('text')


class BoardParticipantFactory(DatesFactoryMixin):
    class Meta:
        model = 'goals.BoardParticipant'

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)


class GoalCategoryFactory(DatesFactoryMixin):
    class Meta:
        model = 'goals.GoalCategory'

    board = factory.SubFactory(BoardFactory)
    title = factory.Faker('sentence', nb_words=5)
    user = factory.SubFactory(UserFactory)


class GoalFactory(DatesFactoryMixin):
    class Meta:
        model = 'goals.Goal'

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)
    title = factory.Faker('sentence', nb_words=5)


class GoalCommentFactory(DatesFactoryMixin):
    class Meta:
        model = 'goals.GoalComment'

    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
    text = factory.Faker('text')

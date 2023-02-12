import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


USER_MODEL = get_user_model()


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture
def get_auth_client(client):
    def _get_auth_client(user):
        client.force_login(user)
        return client

    return _get_auth_client


@pytest.fixture
def auth_client(get_auth_client, test_user):
    return get_auth_client(test_user)


@pytest.fixture
def test_user(db):
    user = USER_MODEL.objects.create(
        username='test',
        password='test',
        email='test@test.ru',
    )
    return user


@pytest.fixture
def board_participant(board_participant_factory):
    return board_participant_factory()


@pytest.fixture
def category(board_participant, goal_category_factory):
    return goal_category_factory(
        board=board_participant.board,
        user=board_participant.user
    )


@pytest.fixture
def goal(board_participant, category, goal_factory):
    return goal_factory(user=board_participant.user, category=category)


@pytest.fixture
def comment_goal(board_participant, goal, goal_comment_factory):
    return goal_comment_factory(user=board_participant.user, goal=goal)

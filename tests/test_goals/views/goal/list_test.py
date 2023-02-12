import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_list_goal(get_auth_client, board_participant, goal_factory, category):

    goal_factory.create_batch(
        5,
        user=board_participant.user,
        category=category
    )

    auth_client = get_auth_client(board_participant.user)

    url = reverse('goal_list')
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_list_category_not_owner(auth_client, goal_factory):
    goal_factory.create_batch(5)

    url = reverse('goal_list')
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

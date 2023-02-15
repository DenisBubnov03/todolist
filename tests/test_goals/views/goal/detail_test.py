import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import Goal


@pytest.mark.django_db
def test_goal_detail(get_auth_client, board_participant, goal):

    auth_client = get_auth_client(board_participant.user)

    url = reverse('goal_detail', kwargs={'pk': goal.pk})
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] != Goal.Status.archived


@pytest.mark.django_db
def test_goal_detail_not_auth_user(client, goal):

    url = reverse('goal_detail', kwargs={'pk': goal.pk})
    response = client.get(
        path=url
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': 'Учетные данные не были предоставлены.'
    }


@pytest.mark.django_db
def test_goal_detail_not_owner(auth_client, goal):

    url = reverse('goal_detail', kwargs={'pk': goal.pk})
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'Страница не найдена.'}

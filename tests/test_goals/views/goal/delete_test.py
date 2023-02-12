import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_goal_delete(get_auth_client, goal, board_participant):
    auth_client = get_auth_client(board_participant.user)

    url = reverse('goal_detail', kwargs={'pk': goal.pk})
    response = auth_client.delete(path=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None


@pytest.mark.django_db
def test_goal_delete_with_another_auth_user(auth_client, goal):
    url = reverse('goal_detail', kwargs={'pk': goal.pk})
    response = auth_client.delete(path=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'Страница не найдена.'}


@pytest.mark.django_db
def test_goal_delete_with_no_auth_user(client, goal):
    url = reverse('goal_detail', kwargs={'pk': goal.pk})
    response = client.delete(path=url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': 'Учетные данные не были предоставлены.'
    }

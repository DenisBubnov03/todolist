import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_comment_update(get_auth_client, board_participant, comment_goal):
    data = {
        'text': 'test',
    }

    auth_client = get_auth_client(board_participant.user)

    url = reverse('comment_detail', kwargs={'pk': comment_goal.pk})
    response = auth_client.patch(
        path=url,
        data=data,
        format='json',
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['text'] == data['text']


@pytest.mark.django_db
def test_comment_update_not_owner(auth_client, comment_goal):
    data = {
        'text': 'test',
    }

    url = reverse('comment_detail', kwargs={'pk': comment_goal.pk})
    response = auth_client.patch(
        path=url,
        data=data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'Страница не найдена.'}

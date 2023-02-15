import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_comment_create(get_auth_client, board_participant, goal):
    url = reverse('comment_create')

    payload = {
        'goal': goal.id,
        'text': 'test comment',
    }
    auth_client = get_auth_client(board_participant.user)

    response = auth_client.post(
        path=url,
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['text'] == payload['text']


@pytest.mark.django_db
def test_comment_create_not_auth_user(client, goal):
    url = reverse('comment_create')
    payload = {
        'goal': goal.id,
        'title': 'test goal',
    }

    response = client.post(
        path=url,
        data=payload,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': 'Учетные данные не были предоставлены.'
    }

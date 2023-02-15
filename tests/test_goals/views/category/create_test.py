import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_category_create(get_auth_client, board_participant):
    url = reverse('category_create')

    auth_client = get_auth_client(board_participant.user)

    payload = {
        'title': 'New_category',
        'board': board_participant.board.id,
    }

    response = auth_client.post(
        path=url,
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == payload['title']


@pytest.mark.django_db
def test_category_create_not_auth_user(client):
    url = reverse('category_create')

    payload = {'title': 'New_category'}

    response = client.post(
        path=url,
        data=payload,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': 'Учетные данные не были предоставлены.'
    }

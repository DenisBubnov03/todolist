import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_board_create(auth_client):
    url = reverse('board_create')
    payload = {'title': 'New_board'}
    response = auth_client.post(
        path=url,
        data=payload
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == payload['title']


@pytest.mark.django_db
def test_board_create_not_auth_user(client):
    url = reverse('board_create')
    payload = {'title': 'New_board'}
    response = client.post(
        path=url,
        data=payload
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': 'Учетные данные не были предоставлены.'
    }

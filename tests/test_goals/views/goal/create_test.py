import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_goal_create(get_auth_client, board_participant, category):
    url = reverse('goal_create')

    payload = {
        'category': category.id,
        'title': 'test goal',
    }
    auth_client = get_auth_client(board_participant.user)

    response = auth_client.post(
        path=url,
        data=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == payload['title']


@pytest.mark.django_db
def test_goal_create_not_auth_user(client, category):
    url = reverse('goal_create')
    payload = {
        'category': category.id,
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

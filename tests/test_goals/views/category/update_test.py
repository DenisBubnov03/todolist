import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_category_update(get_auth_client, board_participant, category):
    data = {
        'title': 'test',
    }

    auth_client = get_auth_client(board_participant.user)

    url = reverse('category_detail', kwargs={'pk': category.pk})
    response = auth_client.patch(
        path=url,
        data=data,
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == data['title']


@pytest.mark.django_db
def test_category_update_not_owner(auth_client, category):
    payload = {
        'title': 'test',
    }

    url = reverse('category_detail', kwargs={'pk': category.pk})
    response = auth_client.patch(
        path=url,
        data=payload,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'Страница не найдена.'}

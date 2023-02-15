import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_category_delete(get_auth_client, board_participant, category):

    auth_client = get_auth_client(board_participant.user)

    url = reverse('category_detail', kwargs={'pk': category.pk})
    response = auth_client.delete(path=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None


@pytest.mark.django_db
def test_category_delete_with_another_auth_user(auth_client, category):

    url = reverse('category_detail', kwargs={'pk': category.pk})
    response = auth_client.delete(path=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'Страница не найдена.'}

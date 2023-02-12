import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_board_delete(get_auth_client, board_participant):

    auth_client = get_auth_client(board_participant.user)

    url = reverse('board_detail', kwargs={'pk': board_participant.board.pk})
    response = auth_client.delete(path=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None


@pytest.mark.django_db
def test_board_delete_with_another_auth_user(auth_client, board_participant):

    url = reverse('board_detail', kwargs={'pk': board_participant.board.pk})
    response = auth_client.delete(path=url)

    assert response.status_code == 404
    assert response.data == {'detail': 'Страница не найдена.'}

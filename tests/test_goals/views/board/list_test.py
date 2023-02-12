import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_list_board(auth_client, board_participant_factory, test_user):
    board_participant_factory.create_batch(5, user=test_user)

    url = reverse('board_list')
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_list_board_not_owner(auth_client, board_participant_factory):
    board_participant_factory.create_batch(5)

    url = reverse('board_list')
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

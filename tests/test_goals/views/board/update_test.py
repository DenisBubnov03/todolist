import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import BoardParticipant


@pytest.mark.django_db
def test_board_update(user_factory, get_auth_client, board_participant_factory):
    owner = user_factory()
    board_participant = board_participant_factory(user=owner)
    board_participant2 = board_participant_factory(
        board=board_participant.board,
        role=BoardParticipant.Role.writer
    )
    user3 = user_factory()

    data = {
        'participants': [
            {
                'role': BoardParticipant.Role.reader,  # изменяем редактора на читателя
                'user': board_participant2.user.username
            },
            {
                'role': BoardParticipant.Role.writer,  # добавляем нового участника
                'user': user3.username
            }
        ],
        'title': board_participant.board.title,
    }

    auth_client = get_auth_client(owner)
    url = reverse('board_detail', kwargs={'pk': board_participant.board.pk})

    response = auth_client.patch(
        path=url,
        data=data,
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['participants'][0]['role'] == BoardParticipant.Role.reader
    assert response.data['participants'][1]['role'] == BoardParticipant.Role.writer


@pytest.mark.django_db
def test_board_update_with_another_auth_user(
        user_factory,
        get_auth_client,
        board_participant_factory,
):
    user1 = user_factory()
    user2 = user_factory()
    board_participant = board_participant_factory(user=user1)

    data = {
        'title': 'test board',
    }

    auth_client = get_auth_client(user2)
    url = reverse('board_detail', kwargs={'pk': board_participant.board.pk})
    response = auth_client.put(
        url,
        data=data,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'Страница не найдена.'}

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_comment_detail(get_auth_client, board_participant, comment_goal):

    auth_client = get_auth_client(board_participant.user)

    url = reverse('comment_detail', kwargs={'pk': comment_goal.pk})
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data is not None


@pytest.mark.django_db
def test_comment_detail_not_auth_user(client, comment_goal):

    url = reverse('comment_detail', kwargs={'pk': comment_goal.pk})
    response = client.get(
        path=url
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {
        'detail': 'Учетные данные не были предоставлены.'
    }


@pytest.mark.django_db
def test_comment_detail_not_owner(auth_client, comment_goal):

    url = reverse('comment_detail', kwargs={'pk': comment_goal.pk})
    response = auth_client.get(
        path=url
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {'detail': 'Страница не найдена.'}

import pytest
from datetime import datetime
from typing import List
from django.urls import reverse
from rest_framework.fields import DateTimeField
from goals.models import Board
from freezegun import freeze_time

drf_str_datetime = DateTimeField().to_representation


@freeze_time('2023-02-07 16:15:34', tz_offset=-3)
@pytest.mark.django_db
class TestBoardListView:
    url = reverse('board-list')
    frozen_datetime = drf_str_datetime(datetime(2023, 2, 7, 13, 15, 34))

    def test_board_list(self, auth_client, user, board_factory):
        boards: List[Board] = board_factory.create_batch(2, with_owner=user)

        response = auth_client.get(self.url)
        expected_response = [
            {
                'id': boards[0].pk,
                'created': self.frozen_datetime,
                'updated': self.frozen_datetime,
                'title': boards[0].title,
                'is_deleted': boards[0].is_deleted,
            },
            {
                'id': boards[1].pk,
                'created': self.frozen_datetime,
                'updated': self.frozen_datetime,
                'title': boards[1].title,
                'is_deleted': boards[1].is_deleted,
            }
        ]

        sorted_response = sorted(response.json(), key=lambda x: x['id'])
        sorted_expected_response = sorted(expected_response, key=lambda x: x['id'])

        assert response.status_code == 200
        assert sorted_response == sorted_expected_response


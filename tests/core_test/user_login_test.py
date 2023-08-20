import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestLoginView:
    url = reverse('core:login')


    def test_invalid_credentials(self, client):
        response = client.post(self.url, data={
            'username': 'wrong_user',
            'password': 'wrong_pwd',
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN


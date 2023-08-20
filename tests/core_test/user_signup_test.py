import pytest
from django.urls import reverse
from rest_framework import status
from core.models import User
from unittest.mock import ANY


@pytest.mark.django_db
class TestSignUpView:
    url = reverse('core:signup')

    from django.contrib.auth.models import User

    def test_user_signup(self, client, user_factory):
        user_data = {  # используйте словарь для упрощения создания POST запроса
            'username': "test_username",
            'password': "test_password_12345",
            'password_repeat': "test_password_12345",
            'first_name': "test_first_name",
            'last_name': "test_last_name",
            'email': "test@example.com",
        }
        response = client.post(self.url, data=user_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        created_user = User.objects.get(
            username=user_data['username'])

        assert created_user.username == user_data['username']
        assert created_user.password is not None
        assert created_user.check_password(user_data['password'])
        assert created_user.first_name == user_data['first_name']
        assert created_user.last_name == user_data['last_name']
        assert created_user.email == user_data['email']

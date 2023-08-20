import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUpdatePasswordView:
    url = reverse('core:update_password')

    def test_user_update_password_success(self, auth_client, faker, user_factory):
        original_password = "SomeStrongPassword123!"
        user = user_factory.create(password=original_password)
        auth_client.force_authenticate(user=user)
        new_password = faker.password()
        response = auth_client.put(self.url, data={
            'old_password': original_password,
            'new_password': new_password,
            'new_password_confirm': new_password
        })

        print(response.content)
        expected_response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }

        assert response.status_code == 200

    def test_user_update_password_wrong(self, auth_client, faker):
        response = auth_client.put(self.url, data={
            'old_password': 'wrong_password',
            'new_password': faker.password(),
            'new_password_confirm': faker.password()
        })
        expected_response = {
            'old_password': [
                'Password is incorrect'
            ]
        }

        assert response.status_code == 400
        assert response.json() == expected_response

    def test_user_update_password_short_numeric(self, auth_client):
        response = auth_client.put(self.url, data={
            'old_password': 'test_pwd',
            'new_password': '1269462',
            'new_password_confirm': '1269462'
        })
        expected_response = {
            'non_field_errors': [
                'This password is too short. It must contain at least 8 characters.',
                'This password is entirely numeric.'
            ]
        }

        assert response.status_code != 200, "Password change succeeded when it should have failed."

        assert response.status_code == 400
        assert response.json() == expected_response

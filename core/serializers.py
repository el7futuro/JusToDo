from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from core.models import User
from rest_framework.exceptions import AuthenticationFailed
from core.fields import PasswordField


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для регистрации пользователя
    """
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat")

    def validate(self, attrs: dict) -> dict:
        """
        Проверка на совпадение введенных паролей
        """
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords must match'})
        return attrs

    def create(self, validated_data: dict) -> User:
        """
        Сохранение пользователя в БД
        """
        validated_data['password'] = make_password(validated_data['password'])
        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """    Сериалайзер для авторизации и аутентификации пользователя
    """
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")
        read_only_fields = ("id", "first_name", "last_name", "email")

    def create(self, validated_data: dict) -> User:
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )
        if not user:
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для отображения данных пользователя
    """
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Сериалайзер для смены пароля
    """
    model = User

    old_password = PasswordField(required=True, write_only=True)
    new_password = PasswordField(required=True, write_only=True)
    new_password_confirm = PasswordField(required=True, write_only=True)

    def validate(self, data):
        new_password = data['new_password']
        new_password_confirm = data['new_password_confirm']

        if new_password != new_password_confirm:
            raise serializers.ValidationError({"new_password_confirm": "Пароли не совпадают"})

        validate_password(new_password)

        return data

    def validate_old_password(self, old_password: str) -> str:
        """
        Проверка корректности ввода старого пароля
        """
        if not self.instance.check_password(old_password):
            raise ValidationError('Password is incorrect')
        return old_password

    def update(self, instance: User, validated_data: dict) -> User:
        """
        Сохранение нового пароля
        """
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    def create(self, validated_data):
        pass
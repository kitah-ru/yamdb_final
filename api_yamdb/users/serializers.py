from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


class UserTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения кода подтверждения."""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя "me" запрещено!')
        return value


class AccessTokenSerializer(TokenObtainSerializer):
    """Сериализатор для получения токена."""

    confirmation_code = serializers.CharField(required=False)

    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = serializers.HiddenField(default='')

    def validate(self, attrs):
        self.user = get_object_or_404(User, username=attrs['username'])

        if attrs.get('confirmation_code') != self.user.confirmations_code:
            raise serializers.ValidationError('Неверный код подтверждения!')

        data = str(self.get_token(self.user))
        return {'token': data}


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя "me" запрещено!')
        return value

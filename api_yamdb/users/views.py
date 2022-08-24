from uuid import uuid4

from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import AdminOnly
from users.serializers import (AccessTokenSerializer,
                               UserSerializer, UserTokenSerializer)


class UserTokenViewSet(CreateModelMixin, GenericViewSet):
    """Вьюсет для получения кода подтверждения."""

    queryset = User.objects.all()
    serializer_class = UserTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = serializer.initial_data.get('username')
        email = serializer.initial_data.get('email')
        if not (username and email):
            serializer.is_valid(raise_exception=True)

        if User.objects.filter(username=username).exists():
            instance = User.objects.get(username=username)
            if not instance.email == email:
                raise ValidationError('У данного пользователя другая почта!')
            serializer.is_valid(raise_exception=False)
        else:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            instance.set_unusable_password()
            instance.save()
            email = serializer.validated_data['email']

        uuid_code = uuid4()
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {uuid_code}',
            'admin@yamdb.ru',
            [email],
            fail_silently=False
        )
        instance.confirmations_code = uuid_code
        instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_200_OK, headers=headers)


class AccessTokenView(TokenObtainPairView):
    """Вьюсет для получения токена."""

    serializer_class = AccessTokenSerializer


class UserViewSet(ModelViewSet):
    """Вьюсет для эндпоинтов с пользователями."""

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly)
    # pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'], detail=False, url_path='me',
            permission_classes=(IsAuthenticated,))
    def personal_profile(self, request):
        """Создать эндпоинт с личной страницей."""
        user = self.request.user
        serializer = UserSerializer(user)

        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                if not serializer.validated_data.get('role'):
                    serializer.save()
        return Response(serializer.data)

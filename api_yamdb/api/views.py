from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.filters import MyFilterSet
from api.permissions import AdminOrReadOnly, IsAuthorModAdmOrReadOnly
from api.serializers import (CategorySerializer, CommentsSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)
from reviews.models import Category, Comments, Genre, Title, Review


class CategoryGenreViewSet(CreateModelMixin, DestroyModelMixin,
                           ListModelMixin, GenericViewSet):
    """Общий вьюсет для категорий и жанров."""

    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CategoryGenreViewSet):
    """Вьюсет для эндпоинта с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CategoryGenreViewSet):
    """Вьюсет для эндпоинта с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(ModelViewSet):
    """Вьюсет для эндпоинта с произведениями."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MyFilterSet


class ReviewViewSet(ModelViewSet):
    """Вьюсет для эндпоинта с отзывами к произведению."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorModAdmOrReadOnly)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ModelViewSet):
    """Вьюсет для эндпоинта с комментариями к отзыву."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorModAdmOrReadOnly)
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs['title_id'],
            id=self.kwargs['review_id']
        )
        return Comments.objects.filter(review=review)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title__id=title_id, id=review_id)
        serializer.save(author=self.request.user, review=review)

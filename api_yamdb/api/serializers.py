from datetime import date
from json import dumps, loads

from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comments, Genre, Review, Title


class SlugWithNameRelatedField(serializers.SlugRelatedField):
    """Класс поля SlugRelated с добавленным атрибутом name."""

    def to_representation(self, obj):
        slug = getattr(obj, self.slug_field)
        query = self.get_queryset().get(slug=slug)

        data = {
            'name': query.name,
            'slug': query.slug
        }
        data = dumps(data)
        data = loads(data)
        return data


class GenreSerializer(serializers.ModelSerializer):
    """"Сериалайзер для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """"Сериалайзер для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """"Сериалайзер для произведений."""

    rating = serializers.SerializerMethodField(read_only=True)
    genre = SlugWithNameRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = SlugWithNameRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        """Проверить, что год произведения не больше текущего."""
        if value >= date.today().year:
            raise serializers.ValidationError(
                'А сегодня в завтрашний день не все могут смотреть...'
            )
        return value

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score')).get('score__avg')


class ReviewSerializer(serializers.ModelSerializer):
    """"Сериалайзер для отзывов к произведению."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):

        if not self.partial and self.context['request'].user.reviews.filter(
            title_id=self.context['view'].kwargs['title_id']
        ).exists():
            raise serializers.ValidationError('Нельзя оставить отзыв дважды!')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """"Сериалайзер для комментариев к отзыву."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments

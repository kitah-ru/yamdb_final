from django_filters import CharFilter, FilterSet

from reviews.models import Title


class MyFilterSet(FilterSet):
    """Фильтерсет для изменения имени полей жанров и категорий."""

    name = CharFilter(field_name='name', lookup_expr='contains')
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']

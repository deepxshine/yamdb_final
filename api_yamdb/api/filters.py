from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter('genre__slug', lookup_expr='icontains')
    category = CharFilter('category__slug', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')

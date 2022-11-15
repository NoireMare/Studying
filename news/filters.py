import django_filters
from django.utils import timezone
from django_filters import FilterSet, DateTimeFromToRangeFilter
from django_filters.widgets import RangeWidget
from news.models import UserCategory


from .models import Post


class PostFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='По названию')
    post_author_id__author_id__username = django_filters.CharFilter(lookup_expr='icontains', label='Автору')
    time_add = DateTimeFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}), label='Дате')

    class Meta:
        model = Post
        fields = ['title', 'post_author_id__author_id__username', 'time_add']





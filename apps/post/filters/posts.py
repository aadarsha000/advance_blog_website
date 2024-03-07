import django_filters
from django.db import models

from ..models import Post


class PostFilter(django_filters.FilterSet):
    order = django_filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        )
    )

    search = django_filters.CharFilter(
        method="filter_search",
        label="Search",
    )

    class Meta:
        model = Post
        fields = {
            "title": ["icontains"],
            "author": ["exact"],
            "category": ["exact"],
            "featured": ["exact"],
            "status": ["exact"],
            "likes": ["exact"],
            "created_at": ["exact", "gte", "lte", "year", "month", "day"],
            "updated_at": ["exact", "gte", "lte", "year", "month", "day"],
        }

    def filter_search(self, queryset, name, value):
        return queryset.filter(models.Q(title__icontains=value))

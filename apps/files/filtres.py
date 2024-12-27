import django_filters
from .models import File

class FileFilter(django_filters.FilterSet):
    file_name = django_filters.CharFilter(method='filter_by_name', label='File Name')
    file_extension = django_filters.CharFilter(method='filter_by_extension', label='File Extension')
    uploaded_at = django_filters.DateFilter(field_name='uploaded_at', lookup_expr='exact')
    uploaded_at__gte = django_filters.DateFilter(field_name='uploaded_at', lookup_expr='gte')
    uploaded_at__lte = django_filters.DateFilter(field_name='uploaded_at', lookup_expr='lte')

    class Meta:
        model = File
        fields = []

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(file__icontains=value)

    def filter_by_extension(self, queryset, name, value):
        return queryset.filter(file__iendswith=f".{value}")

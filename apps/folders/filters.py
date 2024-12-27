import django_filters
from .models import Folder

class FolderFilter(django_filters.FilterSet):
    folderName = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Поиск по названию
    createdAt__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')  # Дата создания >=
    createdAt__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')  # Дата создания <=

    class Meta:
        model = Folder
        fields = ['folderName', 'createdAt__gte', 'createdAt__lte']

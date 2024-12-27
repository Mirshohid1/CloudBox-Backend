from rest_framework.viewsets import ModelViewSet
from ..files.models import File
from ..folders.models import Folder
from ..folders.serializers import FolderSerializer


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

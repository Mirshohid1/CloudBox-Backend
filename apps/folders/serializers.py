from rest_framework import serializers
from .models import Folder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('name', 'parent')


class FolderInputSerializer(serializers.ModelSerializer):
    folderId = serializers.SerializerMethodField
    folderName = serializers.SerializerMethodField
    createdAt = serializers.SerializerMethodField
    parentFolderId = serializers.SerializerMethodField

    class Meta:
        model = Folder
        fields = (
            'folderId', 'folderName',
            'createdAt', 'parentFolderId',
        )

    def get_folderId(self, obj):
        return obj.id

    def get_folderName(self, obj):
        return obj.name

    def get_createdAt(self, obj):
        return obj.created_at

    def get_parentFolderId(self, obj):
        return obj.parent.id

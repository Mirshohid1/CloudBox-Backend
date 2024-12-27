from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('folder', 'file')


class FileInputSerializer(serializers.ModelSerializer):
    fileId = serializers.SerializerMethodField
    fileName = serializers.SerializerMethodField
    fileSize = serializers.SerializerMethodField
    fileType = serializers.SerializerMethodField
    uploadedAt = serializers.SerializerMethodField

    class Meta:
        model = File
        fields = (
            'fileId', 'fileName',
            'fileSize', 'fileType', 'uploadedAt',
        )

    def get_fileId(self, obj):
        return obj.id

    def get_fileName(self, obj):
        return obj.file.name

    def get_fileSize(self, obj):
        return obj.file.size

    def get_uploadedAt(self, obj):
        return obj.uploaded_at

    def get_fileType(self, obj):
        index = obj.file.name.rfind('.')
        return obj.file.name[index + 1:] if index != -1 else 'none'
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from config.utils import data_formatting


class BaseUserInputSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    folders = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'used_storage', 'storage_limit',
            'files', 'folders',
        )

    def get_files(self, obj):
        return obj.files.filter(is_deleted=False).values(
            'id', 'folder', 'file'
            'uploaded_at',
        )

    def get_folders(self, obj):
        return obj.folders.filter(is_deleted=False).values(
            'id', 'name', 'parent',
            'created_at',
        )


class AdminUserInputSerializer(BaseUserInputSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', ''
        )


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate(self, data):
        self._validate_field("username", data.get("username"), User.validate_unique_username)
        self._validate_field("email", data.get("email"), User.validate_unique_email)

        return data

    @staticmethod
    def _validate_field(field_name, value, validation_method):
        if not value:
            raise serializers.ValidationError({field_name: "This field cannot be empty."})
        try:
            data_formatting(value)
            validation_method(value)
        except ValidationError as e:
            raise serializers.ValidationError({field_name: str(e)})

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Topshiriq shartiga ko'ra kam malumot
        data.update({
            'userId': self.user.id
        })

        return data

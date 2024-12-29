from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
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
        try:
            validation_method(value)
        except ValidationError as e:
            raise serializers.ValidationError({field_name: e.message_dict.get(field_name, str(e))})

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
        data.update({
            'userId': self.user.id
        })

        return data

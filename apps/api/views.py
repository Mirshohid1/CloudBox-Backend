from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from apps.files.models import File
from apps.folders.models import Folder
from apps.files.serializers import FileSerializer, FileInputSerializer
from apps.folders.serializers import FolderSerializer, FolderInputSerializer
from apps.users.serializers import CustomTokenObtainPairSerializer, RegisterSerializer


class FileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return File.objects.all()

        return File.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FileSerializer
        return FileInputSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.user != self.request.user:
            raise PermissionDenied("You can't update this file.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can't delete this file.")
        instance.delete()


class FolderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Folder.objects.all()
        return Folder.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FolderSerializer
        return FolderInputSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.user != self.request.user:
            raise PermissionDenied("You can't update this folder.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can't delete this folder.")
        instance.delete()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Вы успешно вышли из системы!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

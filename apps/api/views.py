from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Value, F
from ..files.models import File
from ..files.serializers import FileSerializer, FileInputSerializer
from ..files.filtres import FileFilter
from ..files.pagination import CustomPagination
from ..folders.models import Folder
from ..folders.serializers import FolderSerializer, FolderInputSerializer
from ..folders.pagination import CustomPagination
from ..folders.filters import FolderFilter
from ..users.models import User
from ..users.serializers import CustomTokenObtainPairSerializer, RegisterSerializer


class FolderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Folder.objects.all()
        else:
            return Folder.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action['create', 'update', 'partial_update']:
            return FolderSerializer
        return FolderInputSerializer

    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = FolderFilter
    ordering_fields = ['created_at', 'name']
    ordering = ['created_at']


class FileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return File.objects.all()
        else:
            return File.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FileSerializer
        return FileInputSerializer

    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = FileFilter
    search_fields = ['file']
    ordering_fields = ['file', 'uploaded_at']
    ordering = ['uploaded_at']


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
                'userId': user.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        return Response({
            'token': data.get('access'),
            'userId': data.get('userId')
        }, status=response.status_code)


class CustomLogoutView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({'message': "Muvaffaqiyatli chiqish amalga oshirildi"}, status=status.HTTP_200_OK)
        return response
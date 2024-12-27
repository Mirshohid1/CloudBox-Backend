from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from ..files.models import File
from ..files.serializers import FileSerializer
from ..folders.models import Folder
from ..folders.serializers import FolderSerializer
from ..users.models import User
from ..users.serializers import CustomTokenObtainPairSerializer, RegisterSerializer


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


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
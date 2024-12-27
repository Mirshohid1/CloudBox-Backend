from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views


router = DefaultRouter()
router.register(r'folders', views.FolderViewSet, basename='folder')
router.register(r'files', views.FileViewSet, basename='file')

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/login/', views.CustomTokenObtainPairView.as_view()),
    path('auth/logout/', views.CustomLogoutView.as_view()),
]

urlpatterns += router.urls
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'folders', views.FolderViewSet)
router.register(r'files', views.FileViewSet)

urlpatterns = router.urls
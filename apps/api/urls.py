from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'folders', views.FolderViewSet)

urlpatterns = router.urls
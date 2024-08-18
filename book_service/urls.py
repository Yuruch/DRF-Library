from rest_framework.routers import DefaultRouter

from book_service.views import BookViewSet


router = DefaultRouter()
router.register("", BookViewSet)

urlpatterns = router.urls

app_name = "book_service"

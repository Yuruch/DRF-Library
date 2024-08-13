from rest_framework.routers import DefaultRouter

from borrowings_service.views import BorrowingViewSet

router = DefaultRouter()
router.register("borrowings", BorrowingViewSet)

urlpatterns = router.urls

app_name = "borrowings_service"

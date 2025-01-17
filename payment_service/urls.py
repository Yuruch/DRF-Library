from django.urls import path

from payment_service.views import (
    PaymentListView,
    PaymentDetailView,
    payment_success,
    payment_cancel,
)


app_name = "payment_service"


urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path(
        "<int:pk>/",
        PaymentDetailView.as_view(),
        name="payment-detail",
    ),
    path("success/", payment_success, name="payment-success"),
    path("cancel/", payment_cancel, name="payment-cancel"),
]

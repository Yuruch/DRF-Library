from django.urls import path

from telegram_notification.views import (
    RecieveConfirmationFromTelegram,
)

urlpatterns = [
    path(
        "reviece_telegram_messages/",
        RecieveConfirmationFromTelegram.as_view(),
        name="recieve-messages",
    ),
]

app_name = "telegram-notification"

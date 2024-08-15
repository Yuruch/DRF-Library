from django.urls import path

from telegram_notification.views import ConnectTelegramView, ObtainTelegramConnectionURL

urlpatterns = [
    path(
        "reviece_telegram_messages/",
        ConnectTelegramView.as_view(),
        name="recieve-messages",
    ),
    path(
        "connect_telegram/",
        ObtainTelegramConnectionURL.as_view(),
        name="connect-telegram",
    ),
]

app_name = "telegram-notification"
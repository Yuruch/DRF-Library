import os
import hashlib

from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import views, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from dotenv import load_dotenv

from telegram_notification.telegram_bot import TelegramBot
from telegram_notification.serializer import TelegramUrlSerializer


load_dotenv()

SECRET_PHRASE = os.environ["SECRET_PHRASE"]


class RecieveConfirmationFromTelegram(views.APIView):
    permission_classes = (AllowAny,)

    @extend_schema(exclude=True)
    def post(self, request, *args, **kwargs):
        """Used for receiving confirmation from Telegram API"""
        if not request.data.get("message").get("text").startswith("/start"):
            return Response(status=status.HTTP_204_NO_CONTENT)

        telegram_id = request.data.get("message").get("from").get("id")
        try:
            user_id, signature = (
                request.data.get("message").get("text").split()[1].split("_")
            )
        except ValueError:
            return Response(
                {"error": f"Invalid data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            signature
            != hashlib.sha256(f"{user_id}{SECRET_PHRASE}".encode()).hexdigest()[16:]
        ):
            return Response(
                {"error": f"Invalid signature"}, status=status.HTTP_400_BAD_REQUEST
            )

        user_id = int(user_id)

        try:
            user = get_user_model().objects.get(id=user_id)
            user.telegram_id = telegram_id
            user.save()
            TelegramBot().send_connection_confirm_message_to_user(telegram_id)
            return Response(
                {"status": "Telegram ID connected"}, status=status.HTTP_200_OK
            )
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ObtainTelegramConnectionURL(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TelegramUrlSerializer

    def retrieve(self, request, *args, **kwargs):
        """Obtain the personal URL to connect Telegram"""
        user_id = request.user.id

        signature = hashlib.sha256(f"{user_id}{SECRET_PHRASE}".encode()).hexdigest()[
            16:
        ]
        connect_url = f"{os.environ['BOT_URL']}?start={user_id}_{signature}"
        return Response({"url": connect_url}, status=status.HTTP_200_OK)

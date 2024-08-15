import os
import hashlib

from django.contrib.auth import get_user_model
from rest_framework import views, status
from rest_framework.response import Response
from telegram_notification.telegram_bot import TelegramBot
from dotenv import load_dotenv


load_dotenv()

SECRET_PHRASE = os.environ["SECRET_PHRASE"]


class ConnectTelegramView(views.APIView):
    def post(self, request, *args, **kwargs):
        if not request.data.get("message").get("text").startswith("/start"):
            return Response(status=status.HTTP_204_NO_CONTENT)

        telegram_id = request.data.get("message").get("from").get("id")
        user_id, signature = (
            request.data.get("message").get("text").split()[1].split("#")
        )

        if not telegram_id or not user_id or not user_id.isnumeric() or not signature:
            return Response(
                {"error": f"Invalid data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (
            signature
            != hashlib.sha256(f"{user_id}{SECRET_PHRASE}".encode()).hexdigest()
        ):
            return Response(
                {"error": f"Invalid signature"}, status=status.HTTP_403_FORBIDDEN
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


class ObtainTelegramConnectionURL(views.APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        signature = hashlib.sha256(f"{user_id}{SECRET_PHRASE}".encode()).hexdigest()
        connect_url = f"{os.environ['BOT_URL']}?start={user_id}#{signature}"
        return Response(
            {"your url to connect telegram": connect_url}, status=status.HTTP_200_OK
        )
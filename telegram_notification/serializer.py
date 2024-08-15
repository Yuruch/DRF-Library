from rest_framework import serializers


class TelegramUrlSerializer(serializers.Serializer):
    url = serializers.URLField(
        help_text="Url for connection your account with Telegram", read_only=True
    )

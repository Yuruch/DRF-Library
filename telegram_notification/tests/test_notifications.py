from unittest.mock import patch, MagicMock

from django.test import TestCase

from book_service.models import Book
from borrowings_service.models import Borrowing
from telegram_notification.telegram_bot import TelegramBot
from user.models import User


class TelegramBotTestCase(TestCase):
    @patch("telegram_notification.telegram_bot.requests.post")
    @patch("telegram_notification.telegram_bot.logging.warning")
    def test_borrow_administration_notification(
        self, mock_logging_warning, mock_requests_post
    ):
        mock_borrowing = MagicMock(spec=Borrowing)
        mock_borrowing.borrow_date = "2024-08-15"
        mock_borrowing.expected_return_date = "2024-08-20"
        mock_borrowing.book = MagicMock(spec=Book)
        mock_borrowing.book.__str__.return_value = "Some Book"
        mock_borrowing.user = MagicMock(spec=User)
        mock_borrowing.user.__str__.return_value = "John Doe"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests_post.return_value = mock_response

        bot = TelegramBot()

        bot.borrow_administration_notification(mock_borrowing)

        expected_message = (
            "Borrow date: 2024-08-15\n"
            "Expected return date: 2024-08-20\n"
            "Book: Some Book\n"
            "User: John Doe"
        )
        mock_requests_post.assert_called_once_with(
            f"{bot.base_url}/sendMessage",
            params={"chat_id": bot._chat_id, "text": expected_message},
            headers={"Content-Type": "application/json"},
        )

        mock_logging_warning.assert_not_called()

        mock_response.status_code = 500
        bot.borrow_administration_notification(mock_borrowing)
        mock_logging_warning.assert_called_once_with(
            f"Message is not send: {mock_response.content}"
        )

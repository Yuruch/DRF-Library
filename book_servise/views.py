from rest_framework import viewsets

from book_servise.models import Book
from book_servise.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

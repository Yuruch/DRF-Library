from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from book_service.models import Book
from book_service.permissions import IsAdminOrReadOnly
from book_service.serializers import (
    BookSerializer,
    BookImageSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    """Endpoints of the books in library with basic CRUD operations"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "author"]
    filterset_fields = ["cover"]

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookDetailSerializer

        if self.action == "upload_image":
            return BookImageSerializer

        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to a specific book"""
        book = self.get_object()
        serializer = BookImageSerializer(book, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter books by title (ex. ?title=Python Cookbook)",
            ),
            OpenApiParameter(
                name="author",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter books by author (ex. ?author=David Beazley & Brian K. Jones)",
            ),
            OpenApiParameter(
                name="cover",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter books by cover type (ex. ?cover=SOFT)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

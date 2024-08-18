import os
import uuid

from django.db import models
from django.utils.text import slugify


def book_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    title = instance.title[:50]
    filename = f"{slugify(title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/books/", filename)


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = ("HARD", "Hard cover")
        SOFT = ("SOFT", "Soft cover")

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=Cover.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, upload_to=book_image_file_path)

    class Meta:
        unique_together = (("title", "author"),)

    def __str__(self):
        return self.title

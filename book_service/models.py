from django.db import models


class Book(models.Model):
    class Cover(models.TextChoices):
        HARD = ("HARD", "Hard cover")
        SOFT = ("SOFT", "Soft cover")

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=Cover.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title

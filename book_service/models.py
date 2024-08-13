from django.db import models


class Book(models.Model):
    COVER = [
        ("HARD", "Hard cover"),
        ("SOFT", "Soft cover")
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title

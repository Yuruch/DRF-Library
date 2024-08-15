# Generated by Django 5.1 on 2024-08-14 12:02

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("borrowings_service", "0003_alter_borrowing_borrow_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "Pending"), ("PAID", "Paid")],
                        default="PENDING",
                        max_length=7,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PAYMENT", "Payment"), ("FINE", "Fine")], max_length=7
                    ),
                ),
                ("session_url", models.URLField()),
                ("session_id", models.CharField(max_length=255)),
                (
                    "money_to_pay",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                (
                    "borrowing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="borrowings_service.borrowing",
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 5.1 on 2024-08-14 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings_service", "0002_alter_borrowing_borrow_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
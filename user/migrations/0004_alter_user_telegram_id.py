# Generated by Django 5.1 on 2024-08-15 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_user_telegram_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="telegram_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.1.1 on 2022-10-18 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_otp_verification_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="otp",
            name="status",
            field=models.CharField(
                choices=[("pending", "pending"), ("approved", "approved")],
                default="pending",
                max_length=255,
            ),
        ),
    ]
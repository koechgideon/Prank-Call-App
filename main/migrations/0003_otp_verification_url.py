# Generated by Django 4.1.1 on 2022-10-18 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_otp_tokens"),
    ]

    operations = [
        migrations.AddField(
            model_name="otp",
            name="verification_url",
            field=models.URLField(null=True),
        ),
    ]

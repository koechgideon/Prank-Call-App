from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=14, unique=True)
    tokens = models.IntegerField


def upload_audio(prank, file_name):
    return file_name


def upload_image(prank, image_name):
    return image_name


# Create your models here.
class Prank(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to="image/", blank=True, null=True)
    audio = models.FileField(upload_to="audio/", blank=True, null=True)
    description = models.CharField(max_length=50)


class History(models.Model):
    call_sid = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=14, null=False, blank=False)
    prank = models.ForeignKey(Prank, models.CASCADE, related_name="prank")
    date_created = models.DateField(auto_now_add=True, null=False, blank=True)


class Tokens(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    credits_available = models.IntegerField
    credits_deducted = models.IntegerField
    credits_added = models.IntegerField


class Otp(models.Model):
    # has id
    type = models.CharField(
        max_length=40, blank=False, null=False, choices=settings.OTP_TYPES
    )
    sid = models.CharField(max_length=255, blank=False, null=False)
    verification_url = models.URLField(blank=False, null=True)
    status = models.CharField(
        max_length=255, default="pending", choices=settings.OTP_STATUS
    )
    date_created = models.DateField(auto_now_add=True, null=False, blank=True)


# image, title, sent, likePer, tag;

# class Likes (models.Model):
#     user =  models.ForeignKey(get_user_model(),models.CASCADE)
#     title =  models.CharField(max_length=20)
#     image =  models.ImageField(upload_to = 'image/')
#     audio =  models.FileField(upload_to = 'audio/')
#     description =  models.CharField(max_length=50)


class Tokens (models.Model):
    pass
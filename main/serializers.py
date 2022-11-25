from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError
from utils.images import parse_base64

from main.models import Otp, Prank
from main.twilio_client import client


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "password"]


class PrankSerializer(serializers.HyperlinkedModelSerializer):
    # user = UserSerializer(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def to_internal_value(self, data):
        title = data.get("title", "")

        data["image"] = parse_base64(data.pop("image", None), name=title)
        data["audio"] = parse_base64(data.pop("audio", None), name=title)

        initial = super().to_internal_value(data)

        return initial

    class Meta:
        model = Prank
        fields = ["id", "user", "title", "image", "audio", "description"]


class OtpSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(max_length=14, required=True, write_only=True)

    class Meta:
        model = Otp
        fields = "__all__"
        extra_kwargs = {
            "sid": {"required": False},
            "verification_url": {"required": False},
        }

    def _create_new_twilio_otp(self, validated_data):
        phone_no = validated_data.pop("phone_no", None)
        otpdata = client.verify.v2.services(
            settings.VERIFY_SERVICE_SID
        ).verifications.create(
            to=phone_no,
            channel="sms",
        )

        return {
            **validated_data,
            "sid": otpdata.sid,
            "verification_url": otpdata.url,
        }

    def create(self, validated_data):
        validated_data = self._create_new_twilio_otp(validated_data)

        try:
            instance = self.Meta.model.objects.get(sid=validated_data.get("sid"))
            instance.status = "pending"
            instance.save()
            return instance

        except self.Meta.model.DoesNotExist:
            return super().create(validated_data)


class OtpSerializerVerify(serializers.ModelSerializer):
    instance: Otp
    code = serializers.CharField(max_length=6, required=True, write_only=True)

    class Meta:
        model = Otp
        fields = ["sid", "code", "id"]
        read_only_fields = [
            "sid",
            "id",
        ]

    def validate_code(self, code):
        try:
            client.verify.v2.services(
                settings.VERIFY_SERVICE_SID
            ).verification_checks.create(
                verification_sid=self.instance.sid,
                code=code,
            )

        except Exception as e:
            if settings.DEBUG:
                print(e)
            raise ValidationError("Enter a valid OTP")

    def update(self, instance, validated_data):
        return super().update(instance, {**validated_data, "status": "approved"})

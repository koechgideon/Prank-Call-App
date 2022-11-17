from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import generics, permissions, views, viewsets

from main.twilio_client import client

User = get_user_model()


from main.models import History, Otp, Prank
from main.serializers import (
    OtpSerializer,
    OtpSerializerVerify,
    PrankSerializer,
    UserSerializer,
)


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    # API endpoint that allows users to be viewed or edited.

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrankViewSet(viewsets.ModelViewSet):
    # API endpoint that allows Prank information to be viewed or edited.

    queryset = Prank.objects.all()
    serializer_class = PrankSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MakeCall(views.APIView):
    def post(self, request, *args, **kwargs):
        prank_id = request.data.get("prank_id", None)
        phone_no = request.data.get("phone_no", None)
        if phone_no == None:
            return JsonResponse({"message": "phone is required"}, status=400)
        if prank_id == None:
            return JsonResponse({"message": "prank id is required"}, status=400)
        if not str(prank_id).isdigit():
            return JsonResponse({"message": "prank id is invalid"}, status=400)
        try:
            prank_instance = Prank.objects.get(id=prank_id)
            prank = PrankSerializer(prank_instance).data
            audio_url = prank.get("audio")
        except Exception as e:
            return JsonResponse({"message": "prank does not exist"}, status=400)
        # make a call
        print(phone_no)

        call = client.calls.create(
            record=True,
            # method="GET",
            # status_callback="http://4e39-102-69-225-87.in.ngrok.io/events",
            # status_callback_event=["initiated", "answered"],
            # status_callback_method="POST",
            url="http://9f04-102-69-225-87.in.ngrok.io/media/audio/just-the-3-of-us-prank.mp3",
            # for work owner
            # to="+254715612073",
            # to="+254768379937", # for Bruno
            # to="+254798950450",  # for ceph
            # to="+13392184327", #for Daze Twillio
            # to="+447306107662",  # for Daze
            to=phone_no,
            # to='+18592513806' #for Dommie Twillio
            # from_="+441274015884",  # for Daze
            # from_="+15005550006",
            # from_="+447306107662",  # for Daze
            # from_="+18592513806",  # for Dommie Twillio
            # from_="+447306107672",  # for Daze Personal number
            from_="+13392184327",  # for Daze Twillio
            # from_="+447360278683",  # for Dommie Personal number 447360278683
            twiml="<Response><Play>{audio_url}</Play></Response>".format(
                audio_url=audio_url
            ),
        )

        history = History.objects.create(
            call_sid=call.sid,
            phone_number=call.to,
            user=request.user,
            prank=prank_instance,
        )
        print(vars(history))

        return JsonResponse({"status": "success"})


class _PhoneVerification(views.APIView):
    def post(self, request, *args, **kwargs):
        # phone_no = request.data.get("phone_no", None)
        # otpdata = client.verify.v2.services(
        #     settings.VERIFY_SERVICE_SID
        # ).verifications.create(
        #     to=
        #     # "+254798950450",  # for cephas
        #     # "+254715612073",  # for dommie
        #     # "+254768379937", # for Bruno
        #     phone_no,
        #     channel="sms",
        # )

        OtpSerializer(
            data={
                "sid": otpdata.sid,
                "type": "registration",
            }
        )

        return JsonResponse({"status": "success"})


class PhoneVerification(generics.ListCreateAPIView):
    serializer_class = OtpSerializer
    queryset = Otp.objects.all()


class OtpSerializerVerifyView(generics.RetrieveUpdateAPIView):
    lookup_field = "sid"
    lookup_url_kwarg = "sid"

    serializer_class = OtpSerializerVerify
    queryset = Otp.objects.exclude(status="approved")

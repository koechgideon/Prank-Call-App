from django.urls import include, path
from rest_framework import routers

from main import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"pranks", views.PrankViewSet)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
    path("call/", views.MakeCall.as_view()),
    path("verify/", views.PhoneVerification.as_view()),
    path("verify/<sid>/", views.OtpSerializerVerifyView.as_view()),
]

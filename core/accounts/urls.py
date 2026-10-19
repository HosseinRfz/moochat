from django.urls import path

from .views import (
    RequestPhoneCodeView,
    LoginView,
    CompleteRegistrationView,
)

urlpatterns = [
    path(
        "phone/request-code/",
        RequestPhoneCodeView.as_view(),
        name="request-phone-code",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "register/complete/",
        CompleteRegistrationView.as_view(),
        name="complete-registration",
    ),
]

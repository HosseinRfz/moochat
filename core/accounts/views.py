from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import (
    RegistrationSerializer,
    ActivateAccountSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    LoginSerializer,
)

from .tokens import account_activation_token

User = get_user_model()

password_reset_token = PasswordResetTokenGenerator()


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")

        user = User(**serializer.validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()

        serializer.instance = user

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = f"{settings.FRONTEND_URL}/activate/{uidb64}/{token}/"

        send_mail(
            subject="Account Activation",
            message=f"Click this link to activate your account:\n{activation_link}",
            from_email="noreply@mochat.com",
            recipient_list=[user.email],
        )


class ActivateAccountView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):

        serializer = ActivateAccountSerializer(
            data={
                "uidb64": uidb64,
                "token": token,
            }
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        user.is_active = True
        user.save()

        return Response({"detail": "Account successfully activated."})


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = PasswordResetRequestSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"detail": ("If the email exists, " "a recovery link will be sent")}
            )

        token = password_reset_token.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = (
            f"http://your-frontend.com/reset-password" f"?uid={uid}&token={token}"
        )

        send_mail(
            subject="Password Recovery",
            message=(f"Click this link to recover your password:\n" f"{reset_link}"),
            from_email="noreply@mochat.com",
            recipient_list=[email],
        )

        return Response(
            {"detail": ("If the email exists, " "a recovery link will be sent")}
        )


class PasswordResetConfirmView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = PasswordResetConfirmSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password changed successfully"})

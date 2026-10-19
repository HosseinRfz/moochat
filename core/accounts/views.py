import secrets
import logging

from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from organizations.models import Organization, OrganizationMember

from .serializers import (
    PhoneNumberSerializer,
    LoginSerializer,
    CompleteRegistrationSerializer,
)

User = get_user_model()

logger = logging.getLogger(__name__)


def get_phone_cache_key(phone_number):
    return f"phone_verification:{phone_number}"


def generate_verification_code():
    return f"{secrets.randbelow(1000000):06d}"


def send_verification_code(phone_number, code):
    logger.warning(
        "Verification code for %s: %s",
        phone_number,
        code,
    )


def verify_phone_code(phone_number, code):
    cache_key = get_phone_cache_key(phone_number)
    stored_code = cache.get(cache_key)

    if stored_code is None:
        return False

    if not secrets.compare_digest(str(stored_code), str(code)):
        return False

    cache.delete(cache_key)

    cache.set(
        f"phone_verified:{phone_number}",
        True,
        timeout=3000,
    )

    return True


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RequestPhoneCodeView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]

        code = generate_verification_code()
        cache_key = get_phone_cache_key(phone_number)

        cache.set(cache_key, code, timeout=60)

        send_verification_code(phone_number, code)

        return Response(
            {
                "detail": (
                    "Verification code generated. " "Check the development server logs."
                )
            },
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        code = serializer.validated_data["verification_code"]

        if not verify_phone_code(phone_number, code):
            return Response(
                {"detail": "The verification code is invalid or expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(phone_number=phone_number)

        except User.DoesNotExist:
            cache.set(
                f"phone_verified:{phone_number}",
                True,
                timeout=3000,
            )

            return Response(
                {
                    "detail": "Phone verified. Complete registration.",
                    "registration_required": True,
                    "phone_number": phone_number,
                },
                status=status.HTTP_200_OK,
            )

        if not user.is_active:
            return Response(
                {"detail": "This account is inactive."},
                status=status.HTTP_403_FORBIDDEN,
            )

        tokens = generate_tokens(user)

        return Response(
            {
                **tokens,
                "user": {
                    "id": user.id,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )


class CompleteRegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CompleteRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        phone_number = data["phone_number"]

        if User.objects.filter(phone_number=phone_number).exists():
            return Response(
                {"detail": "This phone number is already registered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Registration requires a recently verified phone number.
        if cache.get(f"phone_verified:{phone_number}") is not True:
            return Response(
                {"detail": "Please verify your phone number first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            user = User.objects.create_user(
                username=phone_number,
                phone_number=phone_number,
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                password=None,
            )

            user.is_active = True
            user.set_unusable_password()
            user.save()

            organization = Organization.objects.create(
                name=data["organization_name"],
                website=data.get("website", ""),
                created_by=user,
            )

            OrganizationMember.objects.create(
                organization=organization,
                user=user,
                role=OrganizationMember.Role.ADMIN,
            )

        cache.delete(f"phone_verified:{phone_number}")

        tokens = generate_tokens(user)

        return Response(
            {
                **tokens,
                "user": {
                    "id": user.id,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "organization": {
                    "id": organization.id,
                    "name": organization.name,
                    "website": organization.website,
                },
            },
            status=status.HTTP_201_CREATED,
        )

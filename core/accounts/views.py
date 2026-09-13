
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import RegistrationSerializer
from .tokens import account_activation_token

User = get_user_model()
password_reset_token = PasswordResetTokenGenerator()


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://your-frontend.com/activate?uid={uid}&token={token}"

        send_mail(
            subject='Account Ativation',
            message=f'Click this link to activate your account:\n{activation_link}',
            from_email='noreply@mochat.com',
            recipient_list=[user.email],
        )


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'detail': 'The link is invalid.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'detail': 'The account has already been activated'})

        if not account_activation_token.check_token(user, token):
            return Response({'detail': 'The token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({'detail': 'Account successfully activated.'})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'If the email exists, a recovery link will be sent'})

        token = password_reset_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://your-frontend.com/reset-password?uid={uid}&token={token}"

        send_mail(
            subject='Password Recovery',
            message=f'Click this link to recover your password:n{reset_link}',
            from_email='noreply@mochat.com',
            recipient_list=[email],)
        return Response({'detail': 'If the email exists, a recovery link will be sent'})



class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({'detail': 'The link is invalid.'}, status=status.HTTP_400_BAD_REQUEST)

        if not password_reset_token.check_token(user, token):
            return Response({'detail': 'The token is invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)
            

        user.set_password(new_password)
        user.save()
        return Response({'detail':'Password changed successfuly'})
from rest_framework import generics, status, views, permissions
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, \
    ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect
import os


# Create your views here.


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(user_id=user_data['user_id'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://' + current_site + relative_link + "?token=" + str(token)

        content = \
            f"""\
                Hello {user.name} {user.surname}\n' \
                We are very happy that you decided to use our page and our services.\n' \
                There is only last step before you can start using cryptostock.com. Click link below to verify your email\n\n' \
                {absurl}\n\n' \
                Thank you for your trust and hope to enjoy your time with us\n\n' \
                Crypto Stock Staff\n\n\n' \
                That message was generated automatically and please do not answer that message. Thank you\n\n'
            """

        alternative_content = \
            f"""\
                <html>
                  <body>
                    <p>Hello {user.name} {user.surname}</p>
                    <p>We are very happy that you decided to use our page and our services.</p>
                    <p>There is only last step before you can start using cryptostock.com. Click link below to verify your email</p>
                    <p></p>
                    <p>{absurl}</p>
                    <p></p>
                    <p>Thank you for your trust and hope to enjoy your time with us</p>
                    <p></p>
                    <p>Crypto Stock Staff</p>
                    <p></p>
                    <p></p>
                    <p>That message was generated automatically and please do not answer that message. Thank you</p>
                  </body>
                </html>
            """

        data = {
            'to_email': user.email,
            'email_subject': 'Verify your email',
            'content': content,
            'alternative_content': alternative_content
        }

        Util.send_email(data)

        return Response(user_data, status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description="User authentication token",
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(user_id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'message': 'Successfully activated'}, status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation expired'}, status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid64 = urlsafe_base64_encode(smart_bytes(user.user_id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uid64': uid64, 'token': token})
            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://' + current_site + relative_link + "?redirect_url=" + redirect_url

            content = \
                f"""\
                    Hello {user.name} {user.surname}\n' \
                    We have just noticed that you want to change your password.\n' \
                    Click link below to confirm and set your new password\n\n' \
                    {absurl}\n\n' \
                    If you did not want to change your password, please contact with support as soon as possible\n\n' \
                    Crypto Stock Staff\n\n\n' \
                    That message was generated automatically and please do not answer that message. Thank you\n\n'
                """

            alternative_content = \
                f"""\
                    <html>
                        <body>
                            <p>Hello {user.name} {user.surname}</p>
                            <p>We have just noticed that you want to change your password.</p>
                            <p>Click link below to confirm and set your new password</p>
                            <p></p>
                            <p>{absurl}</p>
                            <p></p>
                            <p>If you did not want to change your password, please contact with support as soon as possible</p>
                            <p></p>
                            <p>Crypto Stock Staff</p>
                            <p></p>
                            <p></p>
                            <p>That message was generated automatically and plane do not answer that message. Thank you</p>
                        </body>
                    </html>
                """

            data = {
                'to_email': user.email,
                'email_subject': 'Reset your password',
                'content': content,
                'alternative_content': alternative_content
            }

            Util.send_email(data)

        return Response({"success": "We have just sent you a link to reset your password"}, status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uid64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            user_id = smart_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(user_id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uid64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response({
            "success": True,
            "message": "Password has just been changed"},
            status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthUserAPIView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = User.objects.get(user_id=request.user.user_id)
        serializer = RegisterSerializer(user)

        return Response(serializer.data)

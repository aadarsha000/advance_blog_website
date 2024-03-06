from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import UserSerializers, RegisterSerializer
from ..services.email_verification import send_verification_email

User = get_user_model()


class CustomRegisterAPIView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(
                {
                    "success": "User Created Successfully",
                    # "data": UserSerializers(user).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginAPIView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                return Response(
                    {"error": "Username and Password are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = authenticate(email=email, password=password)
            if not user:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not user.is_verified:
                send_verification_email(user, request)
                return Response(
                    {"success": "Please verify your email for login"},
                    status=status.HTTP_200_OK,
                )

            refresh = RefreshToken.for_user(user)
            serializer = UserSerializers(user)
            return Response(
                {
                    "data": {
                        "user_info": serializer.data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):

    def post(self, request):
        user_id = request.data.get("user_id")
        token = request.data.get("otp")

        try:
            user = User.objects.get(id=user_id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"error": "user does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user is not None and default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response(
                {"message": "Successfully verified email."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

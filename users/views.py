from .serializers import SignUpSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, RegisterSerializer

class LoginApiView(APIView):
    def post(self, request):
        request_data = request.data
        serializer = LoginSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**request_data)

        if user is None:
            result = {
                "status": "False",
                "message": "User not found"
            }
            return Response(result)
        else:
            refresh = RefreshToken.for_user(user)

            data = {
                "Refresh": str(refresh),
                "Access": str(refresh.access_token)
            }
            return Response(data)

class RegisterApiView(APIView):
    def post(self, request):
        request_data = request.data
        serializer = RegisterSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = {
            "status": True,
            "message": f"{user.username} is Registered"
        }
        return Response(data)

class SignUpApiView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class VerifyCodeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        if 'code' not in request.data:
            data = {
                "status":False,
                "message":"Code field is required"
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        code = request.data['code']
        if len(code)!=5:
            data = {
                "status":False,
                "message":"Code uzunligi 5ga teng bo'lishi kerak",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        result = user.verification_codes.objects.filter(is_verified=False, expire_time__gte=datetime.now(),code=code).first()
        if result is None:
            data = {
                "status":False,
                "message":"Codeni boshqatdan kiriting",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(user)
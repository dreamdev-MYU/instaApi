from .serializers import SignUpSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CodeVerification
from datetime import datetime

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
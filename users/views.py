from django.shortcuts import render
from .serializers import SignUpSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class SignUpApiView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


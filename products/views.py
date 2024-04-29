from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products
from rest_framework import generics
from .serializers import ProductSerializer



class CreateProductView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateProductView(generics.RetrieveUpdateAPIView):
    queryset = Products.objects.all()
    serializer_class=ProductSerializer


class ReadProductView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class DeleteProductView(generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    


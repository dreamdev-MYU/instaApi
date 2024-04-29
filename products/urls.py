from django.urls import path
from .views import (CreateProductView, ReadProductView, UpdateProductView, DeleteProductView)

urlpatterns = [
    path('create/', CreateProductView.as_view(), name='create-product'),
    path('read/', ReadProductView.as_view(), name = 'read-product'),
    path('update/', UpdateProductView.as_view(), name='update-product'),
    path('delete/', DeleteProductView.as_view(), name = 'delete-product'),
]

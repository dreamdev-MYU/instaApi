from django.urls import path
from .views import SignUpApiView
urlpatterns = [
    path('sign-up/', SignUpApiView.as_view(), name='SignUp')
]

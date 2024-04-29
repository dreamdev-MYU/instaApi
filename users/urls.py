from django.urls import path
from .views import SignUpApiView
from .views import LoginApiView, RegisterApiView


app_name = 'users'

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('sign-up/', SignUpApiView.as_view(), name='SignUp')
]
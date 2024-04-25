from django.urls import path
from .views import SignUpApiView, VerifyCodeApiView
urlpatterns = [
    path('sign-up/', SignUpApiView.as_view(), name='SignUp')
    

]


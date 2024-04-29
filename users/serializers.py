from rest_framework import serializers
from .models import User
from .regex_check import is_valid_phone,is_valid_email
from .models import EMAIL,PHONE
from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CodeVerification
from .telegram_send_code import send_sms
from django.contrib.auth.models import User
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, min_length=5)
    password = serializers.CharField(max_length=8, min_length=4)

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=8, min_length=4)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

    def save(self):
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        email = self.validated_data['email']

        if confirm_password != password:
            raise serializers.ValidationError("Passwords don't match!!!")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists in the database")

        user = User.objects.create_user(username=self.validated_data['username'], email=email, password=password)
        return user


class SignUpSerializer(serializers.ModelSerializer):
    phone_or_email =  serializers.CharField(required=True, write_only=True)

    def validate_phone_or_email(self, value):
        if is_valid_phone(value):
            if User.objects.filter(phone_number=value).exists():
                data = {
                "status":False,
                "massage":"phone number already exist"
            }
            raise ValidationError(data)
        
        elif is_valid_email(value):
             if User.objects.filter(email=value).exists():
                data = {
                "status":False,
                "massage":"Email already exist"
            }
                raise ValidationError(data)
        
        return value

    def validate(self, attrs):
        phone_or_email = attrs.get('phone_or_email')

        if is_valid_phone(phone_or_email):
            auth_type = PHONE

        elif is_valid_email(phone_or_email):
            auth_type = EMAIL
        
        else:
            data = {
                "status":False,
                "massage":"Enter a valid email or phone number"
            }

            raise ValidationError(data)
        attrs['auth_type'] = auth_type

        return attrs
    
    def create(self, validated_data):
        phone_or_email = validated_data['phone_or_email']
        auth_type = validated_data['auth_type']

        if is_valid_phone(phone_or_email):

            user=User.objects.create(phone_number = phone_or_email, auth_type=auth_type)
            code=user.create_code(auth_type)
            send_sms(code)
        else:
            user=User.objects.create(email = phone_or_email, auth_type=auth_type)
            code=user.create_code(auth_type)
            send_sms(code)
       
        validated_data['user'] = user  
    
        return validated_data
    def to_representation(self, instance):
        user = instance['user']
        data = {
            "status":True,
            "message":"code sent to your contact",
            "tokens":user.token()
        }

        return data
    
    


class VerifyCodeApiView(APIView):
    def post(self, request):
        code = request.data.get('code')
        auth_type = request.data.get('auth_type')
        phone_or_email = request.data.get('phone_or_email')

        try:
            verification = CodeVerification.objects.get(code=code, auth_type=auth_type)
        except CodeVerification.DoesNotExist:
            return Response({"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        if verification.is_verified:
            return Response({"detail": "Code has already been verified"}, status=status.HTTP_400_BAD_REQUEST)

        if auth_type == 'phone':
            if phone_or_email != verification.phone_number:
                return Response({"detail": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST)
        elif auth_type == 'email':
            if phone_or_email != verification.email:
                return Response({"detail": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Invalid authentication type"}, status=status.HTTP_400_BAD_REQUEST)

     
        verification.is_verified = True
        verification.save()

        return Response({"detail": "Code verified successfully"}, status=status.HTTP_200_OK)

    
    

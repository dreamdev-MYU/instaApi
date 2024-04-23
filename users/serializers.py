from rest_framework import serializers
from .models import User
from .regex_check import is_valid_phone,is_valid_email
from .models import EMAIL,PHONE
from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CodeVerification

class SignUpSerializer(serializers.ModelSerializer):
    phone_or_email =  serializers.CharField(required=True, write_only=True)
    # class Meta:
    #     model = User
    #     fields = ['phone', 'email', 'auth_type']

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

        else:
            user=User.objects.create(email = phone_or_email, auth_type=auth_type)
       
        user.create_code(auth_type) 
        validated_data['user'] = user  
    
        return validated_data
    def to_representation(self, instance):
        user = instance['user']

        return user.token()
    
    


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

    
    

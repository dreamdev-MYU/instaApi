from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid,random
from datetime import datetime,timedelta
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done', 'photo_done')
EMAIL, PHONE = ('email', 'phone')



class User(AbstractUser):
    AUTH_STEP = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE),
    )
    AUTH_TYPE = (
        (EMAIL,EMAIL),
        (PHONE, PHONE),
    )
    bio = models.CharField(max_length=1000, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True, db_index=True)
    image = models.ImageField(upload_to='users/', default='users/default.jpeg')
    auth_step = models.CharField(choices=AUTH_STEP, max_length=50, default=NEW)
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPE)


    def clean_username(self):
        if not self.username:
            temp_username = f"instagram-{str(uuid.uuid4()).split('-')[-1]}"
           
            self.username= temp_username

    def clean_password(self):
          if not self.password:
              self.password=f"instagram-{str(uuid.uuid4()).split('-')[-1]}"
             
    def hash_password(self):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)

    def clean_all(self):
        self.clean_username()
        self.clean_password()
        self.hash_password()

    def save(self, *args, **kwargs):
        self.clean()
        super(User,self).save(*args, **kwargs)

    def token(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


    def create_code(self,auth_type):
        code = ''.join([str(random.randint(0,9)) for _ in range(4)])
        CodeVerification.objects.create(
            code=code,
            auth_type= auth_type,
            user_id = self.id
        )
        return code

class CodeVerification(models.Model):
    AUTH_TYPE = (
        (EMAIL,EMAIL),
        (PHONE, PHONE),
    )
    code = models.CharField(max_length=4)
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPE)
    expire_time = models.DateTimeField()
    is_vereified = models.BooleanField(default=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="verification_codes", null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.auth_type == EMAIL:
            self.expire_time = datetime.now()+timedelta(minutes=2)
        else:
            self.expire_time = datetime.now()+timedelta(minutes=2)

        super(CodeVerification, self).save(*args, **kwargs)

    def __str__(self):
        return self.code
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email,password,**extra_fields)


class Address(models.Model):
    latitude = models.DecimalField(max_digits=9,decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9,decimal_places=9, null=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50,null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.area

class users(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    address = models.OneToOneField(Address, blank=True,null=True, on_delete=models.SET_NULL, related_name="user_address")
    image = models.ImageField(null=True, blank=True,default="default.png")
    phone = models.CharField(max_length=50,null=True,blank=True)
    is_customer = models.BooleanField(default=True)
    is_delivery_person = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        # Ensure that only superusers can be created using this method
        extra_fields.setdefault('user_role', 'A')
        extra_fields.setdefault('is_staff', True)

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):
    USER_ROLES = (
        ('C', 'Client'),
        ('A', 'Administrator'),
    )

    LANGUAGE = (('UZ', "Uzbek"),
                ('RU', 'Russiam'))

    full_name = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    user_role = models.CharField(max_length=10, choices=USER_ROLES, default='M')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
    lang = models.CharField(max_length=2, default='UZ', choices=LANGUAGE)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name or self.username

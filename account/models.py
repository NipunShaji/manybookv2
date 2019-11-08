from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class AccountManager(BaseUserManager):
    def create_user(self, email, username, dob, password=None):
        if not email:
            raise ValueError("Email is mandatory.")
        if not username:
            raise ValueError('Username is mandatory.')
        if not dob:
            raise ValueError('DOB is mandatory.')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            dob = dob
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, dob, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            dob = dob,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    email           = models.EmailField(verbose_name="Email", max_length=100, unique=True)
    username        = models.CharField(max_length=30, unique=True)
    date_joined     = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='Last Login', auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    dob             = models.DateField(verbose_name='Date of Birth', default=None)
    userpic         = models.ImageField(upload_to='users/', null=True, blank=True)

    USERNAME_FIELD  = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username','dob']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def age(self):
        today = timezone.now().date()
        return today.year - self.dob.year -((today.month, today.day) < (dob.month, dob.day))

@receiver(pre_delete, sender=Account)
def delete_user(sender, instance, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied

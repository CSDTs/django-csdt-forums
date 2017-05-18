from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render
from django.utils import timezone


from . import imglib




class UserManager(BaseUserManager):
    def create_user(self, email, username, display_name=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not display_name:
            display_name = username
        #AUTH_CHANGES included account__
        if not User.objects.filter(account__username__iexact=username).exists():
            user = self.model(
                email=self.normalize_email(email),
                username=username,
                display_name=display_name
            )
            user.set_password(password)
            user.save()
            return user
        raise ValueError("Account name already used")
    
    def create_superuser(self, email, username, display_name, password):
        user = self.create_user(
            email,
            username,
            display_name,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class FileField(models.FileField):

    def save_form_data(self, instance, data):
        if data is not None:
            file = getattr(instance, self.attname)
            if file != data:
                file.delete(save=False)
        super(FileField, self).save_form_data(instance, data)


class User(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    display_name = models.CharField(max_length=140)
    bio = models.CharField(max_length=140, blank=True, default="")
    avatar = FileField(blank=True, null=True,upload_to='avatar')
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name", "username"]
    
    def __str__(self):
        return "@{}".format(self.account.username)
    
    def get_short_name(self):
        return self.display_name
    
    def get_long_name(self):
        return "{} (@{})".format(self.display_name, self.account.username)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.avatar:
            imglib.resize_image(self.avatar)


from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)
from django.conf import settings

class UserManager(BaseUserManager):
    """ Custom manager for the user model """
    def create_user(self, email, password=None, **extra_fields):
        """ Create, save and return a new user """
        if not email:
            raise ValueError(
                'Please enter an email address.'
            )
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using= self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """ Create a superuser using above method and other privileges """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Model to represent user in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()
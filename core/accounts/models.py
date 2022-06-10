from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    '''
    Custom user model: uses email instead of username
    '''
    email = models.EmailField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='pictures/', blank=True)

    address = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, default='Ghana')
    facebook = models.URLField(default="https://www.facebook.com/")
    twitter = models.URLField(default="https/www.twitter.com/")
    instagram = models.URLField(default='https://www.instagram.com/')
    linkedIn = models.URLField(default='https://www.linkedin.com/')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def get_image(self):
        return self.photo.url if self.photo else '/assets/img/user.png'

    def __str__(self):
        '''return email if user's name field is empty'''
        return self.name if self.name else self.email

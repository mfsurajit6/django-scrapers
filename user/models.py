from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    """ Custom manager class to create User and Superuser """

    def create_user(self, email, name='', password=None):
        """ Create and return user with name, email and password"""
        if not name:
            raise TypeError('User must have a name')
        if not email:
            raise TypeError('User must have an email')
        if not password:
            raise TypeError('User must have a password')

        user = self.model(name=name, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):
        """Create and retur user with superuser permission """
        user = self.create_user(name=name, email=email, password=password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User Model """

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password', ]
    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser
    
    def clean(self):
        if self.email is not None:
            self.email = self.email.lower()
        return super(User, self).clean()
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return '<User: {}>'.format(self.name)
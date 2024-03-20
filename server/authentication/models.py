import uuid

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):

    def create_user(self, name, surname, email, date_of_birth, sex, password=None):

        if name is None:
            raise TypeError('User has to have a name')
        if surname is None:
            raise TypeError('User has to have a surname')
        if email is None:
            raise TypeError('User has to have an email')
        if date_of_birth is None:
            raise TypeError('User has to have a date of birth')
        if sex is None:
            raise TypeError('User has to have a sex')

        user = self.model(name=name, surname=surname, email=self.normalize_email(email), date_of_birth=date_of_birth,
                          sex=sex)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, surname, email, date_of_birth, sex, password):

        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(name, surname, email, date_of_birth, sex, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = [
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    surname = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    date_of_birth = models.DateField(null=False)
    sex = models.CharField(choices=SEX_CHOICES, null=False, max_length=10)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    balance = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'date_of_birth', 'sex']

    objects = UserManager()

    def __str__(self):
        return self.name + " " + self.surname + " " + self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

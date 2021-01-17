from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.files import FileField
from django.db.models import UniqueConstraint
import os
from django_enumfield import enum
from enum import Enum

class Rate(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    __default__ = FIVE

class Action(enum.Enum):
    UPLOAD = 1
    LOGIN = 2
    LOGOUT = 3
    DOWNLOAD = 4
    DELETE = 5
    SHARE = 6
    RATE = 7

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User need valid email adress")
        if not username:
            raise ValueError("User need valid username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
        )
        user.is_admin = True
        user.is_staff=True
        user.is_superuser = True
        user.save(using = self._db)
        return user



class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name="username", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class FileMod(models.Model):
    owner = models.ForeignKey( Account,blank=True,null=True, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(verbose_name="upload_date", auto_now_add=True)
    fileF = FileField(upload_to="uploads", null=False, blank= False)
    is_public = models.BooleanField(verbose_name="is_public", default=False)
    f_rate = models.IntegerField(verbose_name="file_rate", default=0)
    def __str__(self):
        return os.path.basename(self.fileF.name)

class SharedFile(models.Model):
    fileS = models.ForeignKey(FileMod,primary_key=True, null=False, blank=True, on_delete=models.CASCADE)
    userS = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)

    class Meta:
        UniqueConstraint(fields = ['fileS', 'userS'], name = 'compositepk')


    def __str__(self):
        return self.fileF +" "+ self.userS

class Opinion(models.Model):
    fileS = models.ForeignKey(FileMod,blank=True,primary_key=True, null=False, on_delete=models.CASCADE)
    userS = models.ForeignKey(Account,blank=True, null=False, on_delete=models.CASCADE)
    rate = enum.EnumField(Rate)

    class Meta:
        UniqueConstraint(fields = ['fileS', 'userS'], name = 'compositepk')

class Logs(models.Model):
    userS = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
    action_date = models.DateTimeField(verbose_name="action_date", auto_now_add=True)
    action = enum.EnumField(Action)
    

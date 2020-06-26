from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

class UserManager(BaseUserManager):
  def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
    if not email:
      raise ValueError('Users must have email address')
    if not password
      raise ValueError('Users must have a password')

    user = self.model(
      email=self.normalize_email(email)
    )
    user.set_password(password)
    user.staff = is_staff
    user.admin = is_admin
    useractive = is_active
    user.save(using=save._db)
    return user

  def  create_staff_user(self, email, password=None):
    user = self.create_user(email, password=password , is_staff=True)
    return user

  def  create_superuser(self, email, password=None):
    user = self.create_user(email, password=password , is_staff=True, is_admin=True)
    return user

class User(AbstractBaseUser):
  email = models.EmailField(max_length=255, unique=True)
  active = models.BooleanField(default=True)
  staff = models.BooleanField(default=False)
  admin = models.BooleanField(default=False) 
  objects = UserManager()
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email

  def get_full_name(self):
    return self.email

  def get_short_name(self):
    return self.email

  @property
  def is_staff(self):
    return self.staff

  @property
  def is_admin(self):
    return self.admin
  
  @property
  def is_active(self):
    return self.active

class GuestEmail(models.Model):
  email = models.EmailField()
  active = models.BooleanField(default=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  update = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.email

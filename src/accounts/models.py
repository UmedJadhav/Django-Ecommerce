from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
  email = models.EmailField(max_length=255, unique=True)
  active = models.BooleanField(default=True)
  staff = models.BooleanField(default=False)
  admin = models.BooleanField(default=False) 

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

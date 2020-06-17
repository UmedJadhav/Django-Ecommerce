from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import GuestEmail
# Create your models here.
User = settings.AUTH_USER_MODEL

'''
 An guest email can have 'many' billing profile , but a registered user can have only 1 billing profile
'''

class BillingProfileManager(models.Manager):
  def new_or_get(self, request):
    user = request.user
    guest_email_id = request.session.get('guest_email_id')
    billing_profile = None
    billling_profile_created = False
    if user.is_authenticated():
      billing_profile, billling_profile_created = self.model.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
      guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
      billing_profile, billling_profile_created = self.model.objects.get_or_create(email=guest_email_obj.email)
    else:
      pass
    return billing_profile, billling_profile_created

class BillingProfile(models.Model):
  user = models.OneToOneField(User, null=True, blank=True)
  email = models.EmailField()
  active = models.BooleanField(default=True) 
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  objects = BillingProfileManager()

  def __str__(self):
    return f"Email: {self.email} Updated_at: {self.updated} Active: {self.active}"

# def billing_profile_created_reciever(sender, instance, created, *args, **kwargs):
#   if created:
#     print('Sending to Stripe')
#     instance.customer_id = newID
#     instance.save()

def user_created_reciever(sender, instance, created, *args, **kwargs):
  if created:
    BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_reciever, sender=User)
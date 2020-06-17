import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_order_id_generator

from billing.models import BillingProfile
from carts.models import Cart

# Create your models here.
ORDER_STATUS_CHOICES = (
  ('created', 'Created'),
  ('paid', 'Paid'),
  ('shipped', 'Shipped'),
  ('refunded', 'Refunded')
)

class OrderManager(models.Manager):
  def new_or_get(self, billing_profile, cart_obj):
    created = False
    qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
    if qs.count() == 1:
      order_obj = qs.first()
    else:
      order_obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
      created = True
    return order_obj, created

class Order(models.Model):
  order_id = models.CharField(max_length=120, blank=True)
  billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
  # shipping_addr = 
  # billing_addr = 
  cart = models.ForeignKey(Cart)
  status = models.CharField(max_length=120, default='created', choices= ORDER_STATUS_CHOICES)
  shipping_total = models.DecimalField(default=150.00, max_digits=100, decimal_places=2)
  total = models.DecimalField(default=0.0, max_digits=100, decimal_places=2)
  active = models.BooleanField(default=True)
  objects = OrderManager()

  def __str__(self):
    return self.order_id
  
  def update_total(self):
    cart_total = self.cart.total
    shipping_total = self.shipping_total
    total = math.fsum([cart_total,shipping_total]) # Can add taxes and stuff
    self.total = format(total, '.2f')
    self.save()
    return total

   
def pre_save_created_order_id(sender, instance, *args, **kwargs):
  if not instance.order_id:
    instance.order_id = unique_order_id_generator(instance)
  qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
  if qs.exists():
    qs.update(active=False)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
  if not created:
    cart_obj = instance
    cart_total = cart_obj.total
    cart_id = cart_obj.id
    qs = Order.objects.filter(cart__id=cart_id)
    if qs.count() == 1: # We should have 1 order per cart
      order_obj = qs.first()
      order_obj.update_total()

def post_save_order(sender, instance, created, *args, **kwargs):
  if created:
    instance.update_total()


pre_save.connect(pre_save_created_order_id, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, sender=Order)
  
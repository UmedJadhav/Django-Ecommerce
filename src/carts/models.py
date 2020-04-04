from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product

User = settings.AUTH_USER_MODEL
# Create your models here.

class CartManager(models.Manager):
  def new_or_get(self, request):
    cart_id = request.session.get('cart_id', None)
    qs = self.get_queryset().filter(id=cart_id)
    if qs.count() == 1:
      new_object = False
      cart_obj = qs.first()
      if request.user.is_authenticated() and cart_obj.user is None: # Handles the case where if the anon user logs in , the cart user is updated
        cart_obj.user = request.user
        cart_obj.save()
    else:
      cart_obj = self.new(user=request.user) # Handles both cases of user logged in or anon user
      request.session['cart_id'] = cart_obj.id
      new_object = True
    return cart_obj, new_object

  def new(self, user=None):
    user_obj = None
    if user is not None:
      if user.is_authenticated():
        user_obj = user
    return self.model.objects.create(user=user_obj)

class Cart(models.Model):
  user = models.ForeignKey(User, null=True, blank=True) # Any user(unsigned too) can create a session
  products = models.ManyToManyField(Product, blank=True)
  subtotal = models.DecimalField(default=0.00 , max_digits=100, decimal_places=2)
  total = models.DecimalField(default=0.00 , max_digits=100, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  objects = CartManager()
  
  def __str__(self):
    return str(self.id)

def m2m_cart_reciever(sender, instance, action, *args, **kwargs):
  if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
    products = instance.products.all()
    total = 0
    for product in products:
      total +=  product.price
    if instance.subtotal != total:
      instance.subtotal = total
      instance.save()

def pre_save_cart_reciever(sender, instance, *args, **kwargs):
  if instance.subtotal > 0 :
    instance.total = instance.subtotal
  else:
    instance.total = 0.00

m2m_changed.connect(m2m_cart_reciever, sender=Cart.products.through)
pre_save.connect(pre_save_cart_reciever, sender=Cart)

from django.db import models
from django.conf import settings

from products.models import Product

User = settings.AUTH_USER_MODEL
# Create your models here.

class CartManager(models.Manager):
  def new_or_get(self, request):
    cart_id = request.session.get('cart_id', None)
    qs = self.get_queryset().filter(id=cart_id)
    if qs.count == 1:
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
  total = models.DecimalField(default=0.00 , max_digits=100, decimal_places=2)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  objects = CartManager()
  def __str__(self):
    return str(self.id)

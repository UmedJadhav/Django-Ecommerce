from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from .models import Cart
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile
from accounts.models import GuestEmail

def cart_home(request):
  cart_obj, cart_created = Cart.objects.new_or_get(request)
  return render(request, 'carts/home.html', {"cart": cart_obj}) 

def cart_update(request):
  product_id = request.POST.get('product_id', None)
  if product_id is not None:
    product_obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
      cart_obj.products.remove(product_obj)
    else:
      cart_obj.products.add(product_obj)
    request.session['cart_items'] = cart_obj.products.count()
  return redirect("cart:home")

def checkout_home(request):
  cart_obj, cart_created = Cart.objects.new_or_get(request)
  if cart_created or cart_obj.products.count() == 0:
    return redirect('cart:home')
  order_obj = None
  user = request.user
  billing_profile = None
  login_form = LoginForm()
  guest_form = GuestForm()
  guest_email_id = request.session.get('guest_email_id')

  if user.is_authenticated():
    billing_profile, billling_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
  elif guest_email_id is not None:
    guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
    billing_profile, billling_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
  else:
    pass
  print(billing_profile)
  if billing_profile is not None:
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
 
  context = {
    'object':order_obj,
    'billing_profile': billing_profile,
    'login_form':login_form,
    'guest_form':guest_form
  }
  return render(request, 'carts/checkout.html', context)
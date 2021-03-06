from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm 
from addresses.models import Address
from .models import Cart
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile
from accounts.models import GuestEmail

def cart_detail_api_view(request):
  cart_obj, cart_created = Cart.objects.new_or_get(request)
  products = [{
              'name': x.name , 'price':x.price ,
              'url': x.get_absolute_url() ,
              'id': x.id
              }
              for x in cart_obj.products.all()]
  return JsonResponse({
    'products': products,
    'subtotal': cart_obj.subtotal,
    'total':cart_obj.total
  })

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
      added = False
    else:
      cart_obj.products.add(product_obj)
      added = True 
    request.session['cart_items'] = cart_obj.products.count()
    if request.is_ajax():
      json_data = {
        'added': added,
        'removed' : not added,
        'cartItemCount':cart_obj.products.count()
      }
      return JsonResponse(json_data)
  return redirect("cart:home")

def checkout_home(request):
  cart_obj, cart_created = Cart.objects.new_or_get(request)
  if cart_created or cart_obj.products.count() == 0:
    return redirect('cart:home')
  order_obj = None
  address_qs= None
  login_form = LoginForm()
  guest_form = GuestForm()
  address_form = AddressForm()
  shipping_address_id = request.session.get('shipping_address_id',None)
  billing_address_id = request.session.get('billing_address_id',None)
  billing_profile, billling_profile_created = BillingProfile.objects.new_or_get(request)

  print(billing_profile)
  if billing_profile is not None:
    if request.user.is_authenticated():
      address_qs = Address.objects.filter(billing_profile=billing_profile)

    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    if shipping_address_id:
      order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
      del request.session['shipping_address_id']
    elif billing_address_id:
      order_obj.billing_address =  Address.objects.get(id=billing_address_id)
      del request.session['billing_address_id']
    if billing_address_id or shipping_address_id :
      order_obj.save()
  
  if request.method == 'POST' :
    is_done = order_obj.check_done
    if is_done:
      order_obj.mark_paid()
      request.session['cart_items'] = 0
      del request.session['cart_id']
    return redirect('cart:success')

  context = {
    'object':order_obj,
    'billing_profile': billing_profile,
    'login_form':login_form,
    'guest_form':guest_form,
    'address_form':address_form,
    'address_qs': address_qs
  }
  return render(request, 'carts/checkout.html', context)

def checkout_done_view(request):
  return render(request, 'carts/checkout-done.html',{})

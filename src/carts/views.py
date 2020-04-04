from django.shortcuts import render, redirect
from products.models import Product
from .models import Cart

def cart_home(request):
  cart_obj, is_new_obj = Cart.objects.new_or_get(request)
  products = cart_obj.products.all()
  total = 0
  for product in products:
    total +=  product.price
  cart_obj.total = total
  cart_obj.save()
  return render(request, 'carts/home.html',{}) 

def cart_update(request):
  product_id = request.POST.get('product_id', None)
  if product_id is not None:
    product_obj = Product.objects.get(id=1)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
      cart_obj.products.remove(product_obj)
    else:
      cart_obj.products.add(product_obj)
  return redirect("cart:home") 
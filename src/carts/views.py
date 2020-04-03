from django.shortcuts import render
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
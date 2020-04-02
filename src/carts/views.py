from django.shortcuts import render
from .models import Cart

def cart_home(request):
  cart_id = request.session.get('cart_id', None)
  qs = Cart.objects.filter(id=cart_id)
  if qs.count == 1:
    cart_obj = qs.first()
    if request.user.is_authenticated() and cart_obj.user is None: # Handles the case where if the anon user logs in , the cart user is updated
      cart_obj.user = request.user
      cart_obj.save()
  else:
    cart_obj = Cart.objects.new(user=request.user) # Handles both cases of user logged in or anon user
    request.session['cart_id'] = cart_obj.id
  return render(request, 'carts/home.html',{})
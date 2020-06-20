from django.shortcuts import render, redirect
from addresses.forms import AddressForm
from django.utils.http import is_safe_url
from billing.models import BillingProfile
from .models import Address

def checkout_address_create_view(request):
  address_form = AddressForm(request.POST or None)
  context = {
    'form' : address_form
  }
  _next = request.GET.get('next')
  _next_post = request.POST.get('next')
  redirect_path = _next or _next_post or None
  if address_form.is_valid():
    print(request.POST)
    print(address_form.cleaned_data)
    instance = address_form.save(commit=False)
    billing_profile,  _ = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None :
      address_type = request.POST.get('address_type','shipping')
      instance.billing_profile = billing_profile
      instance.address_type = address_type
      instance.save()
      request.session[address_type+'_address_id'] = instance.id
      print(address_type+'_address_id',request.session[address_type+'_address_id'])
    else:
      print('Error occured')
      redirect('cart:checkout')
      
    if is_safe_url(redirect_path, request.get_host()):
      return redirect(redirect_path)
  return redirect('cart:checkout')

def checkout_address_reuse_view(request):
  if request.user.is_authenticated():
    context = {}
    _next = request.GET.get('next')
    _next_post = request.POST.get('next')
    redirect_path = _next or _next_post or None
    if request.method == 'POST':
      print(request.POST)
      shipping_address = request.POST.get('shipping_address',None)
      billing_profile,  _ = BillingProfile.objects.new_or_get(request)
      address_type = request.POST.get('address_type','shipping')
      if shipping_address is not None:
        qs = Address.objects.filter(billing_profile = billing_profile, id = shipping_address)
        if qs.exists():
          request.session[address_type+'_address_id'] = shipping_address  
      print(request.session[address_type+'_address_id'])
      if is_safe_url(redirect_path, request.get_host()):
        return redirect(redirect_path)
  return redirect('cart:checkout')

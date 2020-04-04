from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login ,get_user_model

def home_page(request):
  context = {'title': 'Home Page',
            'content': 'Hello world'}
             
  if request.user.is_authenticated():
    context['premium_content']= 'yeah'
  
  return render(request,'home_page.html', context)

def contact_page(request):
  contact_form = ContactForm(request.POST or None)
  context = {'title' : 'Contact',
            'content' : 'Welcome to Contacts Page',
            'form' : contact_form,
            'brand' : 'New Brand name'
            }
  if contact_form.is_valid():
    print(contact_form.cleaned_data)
  # if request.method == 'POST':
  #   print(request.POST)
  return render(request,'contact/view.html', context)

def about_page(request):
  return render(request,'about_page.html',{})


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm, LoginForm, RegisterForm
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

def login_page(request):
  login_form = LoginForm(request.POST or None)
  context = {
    'form':login_form
  }
  print(request.user.is_authenticated())
  if login_form.is_valid():

    print(login_form.cleaned_data)
    context['form'] = LoginForm()

    username = login_form.cleaned_data.get('username')
    password = login_form.cleaned_data.get('password')
    user = authenticate(request, username=username, password=password)
    print(request.user.is_authenticated())

    if user is not None:
      print(request.user.is_authenticated())
      login(request, user)
      context['form'] = LoginForm()
      return redirect('/')
    else:
      print('Error')

  return render(request,'auth/login.html',context)

User = get_user_model()
def register_page(request):
  register_form = RegisterForm(request.POST or None)
  context={'form': register_form,
            }
  if register_form.is_valid():
    print(register_form.cleaned_data)

    username = register_form.cleaned_data.get('username')
    email = register_form.cleaned_data.get('email')
    password = register_form.cleaned_data.get('password')

    new_user = User.objects.create_user(username, email, password)
    print(new_user)
  return render(request,'auth/register.html', context)
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm

def home_page(request):
  return render(request,'home_page.html',{})

def contact_page(request):
  contact_form = ContactForm(request.POST or None)
  context = {'title' : 'Contact',
            'content' : 'Welcome to Contacts Page',
            'form' : contact_form 
            }
  if contact_form.is_valid():
    print(contact_form.cleaned_data)
  # if request.method == 'POST':
  #   print(request.POST)
  return render(request,'contact/view.html', context)

def about_page(request):
  return render(request,'about_page.html',{})
  
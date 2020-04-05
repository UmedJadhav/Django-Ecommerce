from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':' Name'}))
  password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':' Name'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs = {'class':'form-control','placeholder':'Your email'}))
  password = forms.CharField(widget=forms.PasswordInput)
  password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

  def clean_username(self):
    username = self.cleaned_data.get('username')
    qs = User.objects.filter(username=username)
    
    if qs.exists():
      raise forms.ValidationError('Username already taken')
    
    return username

  def clean_email(self):
    email = self.cleaned_data.get('email')
    qs = User.objects.filter(email=email)
    
    if qs.exists():
      raise forms.ValidationError('email already taken')
    
    return email

  def clean(self):
    data =  self.cleaned_data
    self.password = data['password']
    self.password2 = data['password2']

    if self.password != self.password2:
      raise forms.ValidationError('Passwords must  match')
    
    return data

class GuestForm(forms.Form):
  email = forms.EmailField()

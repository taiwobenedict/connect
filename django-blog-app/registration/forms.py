
from tkinter import Widget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms
from django.forms.widgets import TextInput


class SignUpForm(UserCreationForm):
  first_name = forms.CharField(required=True, max_length=30, label='Name')
  username = forms.CharField(max_length=30, required=True )
  email = forms.CharField(max_length=30, required=True )
  password1 = forms.CharField(max_length=30, required=True )
  password2 = forms.CharField(max_length=30, required=True )
  
  first_name.widget.attrs.update({'class': 'form-control', 'placeholder':"Full name"})
  username.widget.attrs.update({'class': 'form-control', 'placeholder':"Username *"})
  email.widget.attrs.update(
      {'class': 'form-control', 'placeholder': "Your Email "})
  password1.widget.attrs.update(
      {'class': 'form-control', 'placeholder': "Your Password *"})
  password2.widget.attrs.update(
      {'class': 'form-control', 'placeholder': "Confirm Password *"})

class LoginForm(forms.Form):
  username = forms.CharField(max_length= 30, required= True, widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your username'}))
  password = forms.CharField(max_length=20, widget= forms.PasswordInput(attrs={'class': 'form-control',  'placeholder':'Your password'}),required= True)


class ResetPassword(PasswordResetForm):
    email = forms.EmailField(max_length=30, required=True)
  
    email.widget.attrs.update(
        {'class': 'form-control my-2', 'placeholder': "Your Email "})

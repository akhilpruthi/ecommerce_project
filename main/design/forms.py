# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class ProductForm(forms.ModelForm):
  
    class Meta:
        model = Product
        fields = ['product_brand', 'product_image','product_name', 'product_description', 'product_price', 'product_usage_for']
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'category', 'image', 'price')


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'image', 'price')


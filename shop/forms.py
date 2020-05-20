from django import forms
from .models import Product, Reviews


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'category', 'price', 'image')


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'category', 'price', 'image')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('text',)

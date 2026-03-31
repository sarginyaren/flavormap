from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import MenuItem, Restaurant, RestaurantPhoto, Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'description', 'address', 'phone',
            'price_range', 'category', 'location',
            'photo', 'latitude', 'longitude',
        ]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
        }


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = RestaurantPhoto
        fields = ['image', 'caption']
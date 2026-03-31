from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MenuItemForm, PhotoForm, RegisterForm, RestaurantForm, ReviewForm
from .models import (
    Category, Favorite, Location, MenuItem,
    Restaurant, RestaurantPhoto, Review, ReviewLike, ReviewReply,
)

def home(request):
    restaurants = Restaurant.objects.all().order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'home.html', {'restaurants': restaurants, 'categories': categories})


def restaurant_list(request):
    restaurants = Restaurant.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    price = request.GET.get('price', '')

    if q:
        restaurants = restaurants.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    if price:
        restaurants = restaurants.filter(price_range=price)

    return render(request, 'restaurants/list.html', {
        'restaurants': restaurants,
        'categories': categories,
    })


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    reviews = restaurant.reviews.all().order_by('-created_at')
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant, 'reviews': reviews})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to flavor, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
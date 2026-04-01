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
    top_rated = (
        Restaurant.objects
        .annotate(avg_rating=Avg('reviews__rating'), review_count=Count('reviews'))
        .filter(review_count__gte=1)
        .order_by('-avg_rating')[:6]
    )
    new_arrivals = Restaurant.objects.order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'top_rated': top_rated,
        'new_arrivals': new_arrivals,
        'categories': categories,
    })


def restaurant_list(request):
    restaurants = Restaurant.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews'),
    )
    categories = Category.objects.all()
    cities = Location.objects.values_list('city', flat=True).distinct()

    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    price = request.GET.get('price', '')
    city = request.GET.get('city', '')
    min_rating = request.GET.get('min_rating', '')
    sort = request.GET.get('sort', 'new')

    if q:
        restaurants = restaurants.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(address__icontains=q) |
            Q(location__city__icontains=q) |
            Q(location__district__icontains=q)
        )
    if category_id:
        restaurants = restaurants.filter(category_id=category_id)
    if price:
        restaurants = restaurants.filter(price_range=price)
    if city:
        restaurants = restaurants.filter(location__city=city)
    if min_rating:
        try:
            restaurants = restaurants.filter(avg_rating__gte=float(min_rating))
        except ValueError:
            pass

    if sort == 'rating':
        restaurants = restaurants.order_by('-avg_rating')
    elif sort == 'popular':
        restaurants = restaurants.order_by('-review_count')
    else:
        restaurants = restaurants.order_by('-created_at')

    return render(request, 'restaurants/list.html', {
        'restaurants': restaurants,
        'categories': categories,
        'cities': cities,
    })


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    reviews = (
        restaurant.reviews
        .select_related('user')
        .prefetch_related('replies__author', 'likes')
        .order_by('-created_at')
    )
    photos = restaurant.photos.all().order_by('-created_at')

    user_has_reviewed = False
    user_favorite = False
    user_liked_reviews = set()

    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()
        user_favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()
        user_liked_reviews = set(
            ReviewLike.objects
            .filter(user=request.user, review__restaurant=restaurant)
            .values_list('review_id', flat=True)
        )

    menu_by_cat = {}
    for item in restaurant.menu_items.filter(is_available=True).order_by('category', 'name'):
        label = item.get_category_display()
        menu_by_cat.setdefault(label, []).append(item)

    return render(request, 'restaurants/detail.html', {
        'restaurant': restaurant,
        'reviews': reviews,
        'menu_by_cat': menu_by_cat,
        'photos': photos,
        'user_has_reviewed': user_has_reviewed,
        'user_favorite': user_favorite,
        'user_liked_reviews': user_liked_reviews,
        'review_form': ReviewForm(),
    })


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


@login_required
def restaurant_add(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.created_by = request.user
            restaurant.save()
            messages.success(request, 'Restaurant added successfully!')
            return redirect('restaurant_detail', pk=restaurant.pk)
    else:
        form = RestaurantForm()
    return render(request, 'restaurants/form.html', {'form': form, 'action': 'Add'})


@login_required
def restaurant_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if restaurant.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this restaurant.')
        return redirect('restaurant_detail', pk=pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant updated!')
            return redirect('restaurant_detail', pk=pk)
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'restaurants/form.html', {
        'form': form, 'action': 'Edit', 'restaurant': restaurant,
    })
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
    cities = Location.objects.values_list ('city', flat=True).distinct()

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


@login_required
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if restaurant.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this restaurant.')
        return redirect('restaurant_detail', pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        messages.success(request, 'Restaurant deleted.')
        return redirect('restaurant_list')
    return render(request, 'restaurants/delete_confirm.html', {'restaurant': restaurant})


@login_required
def review_add(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if Review.objects.filter(user=request.user, restaurant=restaurant).exists():
        messages.warning(request, 'You have already reviewed this restaurant.')
        return redirect('restaurant_detail', pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                review = form.save(commit=False)
                review.restaurant = restaurant
                review.user = request.user
                review.author = request.user.username
                review.save()
            messages.success(request, 'Review submitted!')
    return redirect('restaurant_detail', pk=pk)


@login_required
def menu_add(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if restaurant.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'Only the owner can manage the menu.')
        return redirect('restaurant_detail', pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            messages.success(request, 'Menu item added!')
            return redirect('restaurant_detail', pk=pk)
    else:
        form = MenuItemForm()
    return render(request, 'restaurants/menu_form.html', {'form': form, 'restaurant': restaurant})


@login_required
def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    restaurant = item.restaurant
    if restaurant.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'Only the owner can delete menu items.')
        return redirect('restaurant_detail', pk=restaurant.pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Menu item deleted.')
    return redirect('restaurant_detail', pk=restaurant.pk)


@login_required
def toggle_favorite(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    if not created:
        fav.delete()
    return redirect('restaurant_detail', pk=pk)


@login_required
def favorites_list(request):
    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related('restaurant', 'restaurant__category', 'restaurant__location')
        .order_by('-created_at')
    )
    return render(request, 'restaurants/favorites.html', {'favorites': favorites})


@login_required
def profile(request):
    user_reviews = request.user.reviews.select_related('restaurant').order_by('-created_at')
    user_favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related('restaurant')
        .order_by('-created_at')
    )
    user_restaurants = Restaurant.objects.filter(created_by=request.user).order_by('-created_at')
    profile_stats = (user_reviews.count(), user_favorites.count(), user_restaurants.count())
    return render(request, 'profile.html', {
        'user_reviews': user_reviews,
        'user_favorites': user_favorites,
        'user_restaurants': user_restaurants,
        'profile_stats': profile_stats,
    })


@login_required
def reply_add(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            ReviewReply.objects.create(review=review, author=request.user, text=text)
    return redirect('restaurant_detail', pk=review.restaurant.pk)


@login_required
def like_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
    if not created:
        like.delete()
    return redirect('restaurant_detail', pk=review.restaurant.pk)


@login_required
def photo_add(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.restaurant = restaurant
            photo.uploaded_by = request.user
            photo.save()
            messages.success(request, 'Photo uploaded!')
            return redirect('restaurant_detail', pk=pk)
    else:
        form = PhotoForm()
    return render(request, 'restaurants/photo_form.html', {'form': form, 'restaurant': restaurant})
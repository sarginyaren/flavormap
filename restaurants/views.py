from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Restaurant, Category


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

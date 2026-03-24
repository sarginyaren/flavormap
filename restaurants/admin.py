from django.contrib import admin

from .models import Category, Location, Restaurant, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'district']
    list_filter = ['city']
    search_fields = ['city', 'district']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'price_range', 'created_at']
    list_filter = ['category', 'price_range', 'location__city']
    search_fields = ['name', 'description', 'address']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'restaurant']
    search_fields = ['author', 'text']

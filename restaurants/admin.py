from django.contrib import admin

from .models import (
    Category, Favorite, Location, MenuItem,
    Restaurant, RestaurantPhoto, Review, ReviewLike, ReviewReply,
)



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
    list_display = ['name', 'category', 'location', 'price_range', 'created_by', 'created_at']
    list_filter = ['category', 'price_range', 'location__city']
    search_fields = ['name', 'description', 'address']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'restaurant__name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'restaurant']
    search_fields = ['author', 'text']


@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'review', 'created_at']
    search_fields = ['author__username', 'text']


@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'review']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant', 'created_at']
    list_filter = ['restaurant']
    search_fields = ['user__username', 'restaurant__name']


@admin.register(RestaurantPhoto)
class RestaurantPhotoAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'uploaded_by', 'caption', 'created_at']
    search_fields = ['restaurant__name', 'caption']

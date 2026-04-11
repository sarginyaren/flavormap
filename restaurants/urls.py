from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/add/', views.restaurant_add, name='restaurant_add'),
    path('restaurants/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurants/<int:pk>/edit/', views.restaurant_edit, name='restaurant_edit'),
    path('restaurants/<int:pk>/delete/', views.restaurant_delete, name='restaurant_delete'),
    path('restaurants/<int:pk>/review/', views.review_add, name='review_add'),
    path('restaurants/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('restaurants/<int:pk>/menu/add/', views.menu_add, name='menu_add'),
    path('menu/<int:pk>/delete/', views.menu_delete, name='menu_delete'),
    path('review/<int:review_id>/reply/', views.reply_add, name='reply_add'),
    path('review/<int:review_id>/like/', views.like_review, name='like_review'),
    path('restaurants/<int:pk>/photo/', views.photo_add, name='photo_add'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorites_list, name='favorites_list'),
]
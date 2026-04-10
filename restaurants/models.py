from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.district}, {self.city}'


PRICE_CHOICES = [
    ('1', '₺'),
    ('2', '₺₺'),
    ('3', '₺₺₺'),
]


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    price_range = models.CharField(max_length=1, choices=PRICE_CHOICES, default='2')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='restaurants'
    )
    photo = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else None

    def price_display(self):
        return dict(PRICE_CHOICES).get(self.price_range, '₺₺')


MENU_CAT = [
    ('starter', 'Starter'),
    ('main', 'Main Course'),
    ('dessert', 'Dessert'),
    ('drink', 'Drink'),
]


class MenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_items'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=10, choices=MENU_CAT, default='main')
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} ({self.restaurant.name})'


class Review(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews'
    )
    author = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.restaurant.name} ({self.rating})'


class ReviewReply(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_replies'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Review Replies'

    def __str__(self):
        return f'Reply by {self.author.username} on review {self.review.id}'


class ReviewLike(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_likes'
    )

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f'{self.user.username} liked review {self.review.id}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f'{self.user.username} — {self.restaurant.name}'


class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_photos'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo for {self.restaurant.name}'
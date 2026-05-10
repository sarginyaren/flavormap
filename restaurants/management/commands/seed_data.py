from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from restaurants.models import Category, Location, Restaurant, Review

DEFAULT_HOURS = {
    'monday': '08:00-22:00',
    'tuesday': '08:00-22:00',
    'wednesday': '08:00-22:00',
    'thursday': '08:00-22:00',
    'friday': '08:00-23:00',
    'saturday': '09:00-23:00',
    'sunday': '09:00-22:00',
}

LATE_NIGHT_HOURS = {
    'monday': '11:00-23:00',
    'tuesday': '11:00-23:00',
    'wednesday': '11:00-23:00',
    'thursday': '11:00-23:00',
    'friday': '11:00-00:00',
    'saturday': '11:00-00:00',
    'sunday': '12:00-22:00',
}

WEEKDAY_ONLY_HOURS = {
    'monday': '09:00-18:00',
    'tuesday': '09:00-18:00',
    'wednesday': '09:00-18:00',
    'thursday': '09:00-18:00',
    'friday': '09:00-18:00',
    'saturday': '',
    'sunday': '',
}


RESTAURANTS_DATA = [
    {
        'name': 'Starbucks Acibadem',
        'description': 'A cozy Starbucks branch right next to Acibadem University — the perfect spot for studying or catching up with friends over your favorite coffee.',
        'address': 'Acibadem Cad. No:12, Kadikoy',
        'phone': '+90 216 340 10 10',
        'price_range': '2',
        'category': 'Café',
        'opening_hours': DEFAULT_HOURS,
        'reviews': [
            ('Emily', 5, 'Great coffee and very friendly staff. The wifi is fast — perfect for working between classes.'),
            ('James', 4, 'Always consistent quality. Gets a bit crowded during lunch hours.'),
        ],
    },
    {
        'name': "McDonald's Acibadem",
        'description': "Classic McDonald's burgers and fries. Conveniently located near the university with fast service.",
        'address': 'Acibadem Mah. Cevizlik Sok. No:3, Kadikoy',
        'phone': '+90 216 340 20 20',
        'price_range': '1',
        'category': 'Fast Food',
        'opening_hours': LATE_NIGHT_HOURS,
        'reviews': [
            ('Tom', 3, "Standard McDonald's. Nothing surprising but reliable and quick."),
        ],
    },
    {
        'name': 'Durumcu Ahmet Usta',
        'description': 'A beloved local wrap shop famous for its spicy chicken doner and hand-stretched lavash bread. A must-try for any food lover in the area.',
        'address': 'Acibadem Cad. No:47, Kadikoy',
        'phone': '+90 216 341 55 55',
        'price_range': '1',
        'category': 'Kebab',
        'opening_hours': {
            'monday': '10:00-22:00',
            'tuesday': '10:00-22:00',
            'wednesday': '10:00-22:00',
            'thursday': '10:00-22:00',
            'friday': '10:00-23:00',
            'saturday': '10:00-23:00',
            'sunday': '',
        },
        'reviews': [
            ('Mehmet', 5, 'Best doner wrap in the neighborhood. The bread is fresh every day.'),
            ('Sara', 5, 'Huge portions and amazing flavor. I come here every week.'),
        ],
    },
    {
        'name': 'Sushi Co Acibadem',
        'description': 'Modern Japanese restaurant serving fresh sushi rolls, sashimi platters and miso soup. A popular dinner destination for the university crowd.',
        'address': 'Mithatpasa Cad. No:22, Kadikoy',
        'phone': '+90 216 340 77 88',
        'price_range': '3',
        'category': 'Japanese',
        'opening_hours': {
            'monday': '12:00-23:00',
            'tuesday': '12:00-23:00',
            'wednesday': '12:00-23:00',
            'thursday': '12:00-23:00',
            'friday': '12:00-00:00',
            'saturday': '12:00-00:00',
            'sunday': '12:00-22:00',
        },
        'reviews': [
            ('Anna', 5, 'The salmon rolls are exceptional. Great atmosphere and attentive service.'),
            ('David', 4, 'Pricey but worth it for a special occasion. The omakase set was outstanding.'),
        ],
    },
    {
        'name': 'Pizza Express Acibadem',
        'description': 'Authentic Italian-style thin-crust pizzas baked in a stone oven, along with fresh pasta dishes and tiramisu.',
        'address': 'Acibadem Cad. No:61, Kadikoy',
        'phone': '+90 216 342 33 44',
        'price_range': '2',
        'category': 'Italian',
        'opening_hours': LATE_NIGHT_HOURS,
        'reviews': [
            ('Laura', 4, 'Crispy thin crust and generous toppings. The margherita is simple perfection.'),
        ],
    },
    {
        'name': 'Balik Ekmek Corner',
        'description': 'Fresh grilled fish sandwiches made to order with crispy fish fillets, onion and parsley. A classic Istanbul street food experience.',
        'address': 'Acibadem Mah. Karanfil Sok. No:5, Kadikoy',
        'phone': '+90 216 341 11 22',
        'price_range': '1',
        'category': 'Seafood',
        'opening_hours': WEEKDAY_ONLY_HOURS,
        'reviews': [
            ('Chris', 5, 'The freshest fish sandwich I have had. Incredibly affordable too.'),
            ('Nadia', 4, 'Authentic Istanbul flavor. The queue moves fast and it is totally worth the wait.'),
        ],
    },
    {
        'name': 'Teras Cafe & Restaurant',
        'description': 'A charming rooftop café with views of the Bosphorus, serving all-day breakfast, salads and specialty coffees.',
        'address': 'Acibadem Cad. No:88, Kat:3, Kadikoy',
        'phone': '+90 216 343 66 77',
        'price_range': '2',
        'category': 'Café',
        'opening_hours': DEFAULT_HOURS,
        'reviews': [
            ('Sophie', 5, 'The rooftop view is stunning. Perfect for a relaxed weekend brunch.'),
            ('Ali', 4, 'Great coffee and a wonderful vibe. Service can be slow but the view makes up for it.'),
        ],
    },
    {
        'name': 'KFC Acibadem',
        'description': 'Crispy fried chicken, burgers and sides served fast. A reliable option near the university for a quick meal.',
        'address': 'Mithatpasa Cad. No:9, Kadikoy',
        'phone': '+90 216 340 40 40',
        'price_range': '1',
        'category': 'Fast Food',
        'opening_hours': LATE_NIGHT_HOURS,
        'reviews': [
            ('Jake', 3, 'Good crispy chicken. The zinger burger is always satisfying.'),
        ],
    },
    {
        'name': 'Nusret Steakhouse Kadikoy',
        'description': 'Premium steakhouse known for its perfectly seasoned dry-aged cuts and theatrical salt-bae presentation. An unforgettable dining experience.',
        'address': 'Bahariye Cad. No:35, Kadikoy',
        'phone': '+90 216 344 00 00',
        'price_range': '3',
        'category': 'Steakhouse',
        'opening_hours': {
            'monday': '17:00-00:00',
            'tuesday': '17:00-00:00',
            'wednesday': '17:00-00:00',
            'thursday': '17:00-00:00',
            'friday': '17:00-01:00',
            'saturday': '17:00-01:00',
            'sunday': '17:00-23:00',
        },
        'reviews': [
            ('Michael', 5, 'The ribeye was absolutely incredible. Worth every penny for a special night out.'),
            ('Jessica', 5, 'Theatrical and delicious. The staff really know how to make the experience memorable.'),
        ],
    },
    {
        'name': 'Simit Sarayi Acibadem',
        'description': 'A beloved Turkish bakery chain offering freshly baked simit (sesame bagels), pastries and Turkish tea — ideal for a quick and affordable breakfast.',
        'address': 'Acibadem Cad. No:5, Kadikoy',
        'phone': '+90 216 341 00 99',
        'price_range': '1',
        'category': 'Bakery',
        'opening_hours': {
            'monday': '06:30-21:00',
            'tuesday': '06:30-21:00',
            'wednesday': '06:30-21:00',
            'thursday': '06:30-21:00',
            'friday': '06:30-22:00',
            'saturday': '07:00-22:00',
            'sunday': '07:00-20:00',
        },
        'reviews': [
            ('Zeynep', 5, 'Fresh simit every morning. The cheese borek is a must. Perfect before morning lectures.'),
            ('Can', 4, 'Classic Turkish breakfast stop. Cheap, fast and always fresh.'),
        ],
    },
]


USERS_DATA = [
    {'username': 'esin', 'email': 'esin@flavor.com', 'password': 'flavor123', 'is_superuser': False},
    {'username': 'rana', 'email': 'rana@flavor.com', 'password': 'flavor123', 'is_superuser': False},
    {'username': 'ramiz', 'email': 'ramiz@flavor.com', 'password': 'flavor123', 'is_superuser': False},
    {'username': 'yaren', 'email': 'yaren@flavor.com', 'password': '123456', 'is_superuser': False},
    {'username': 'admin', 'email': 'admin@flavor.com', 'password': 'admin123', 'is_superuser': True},
]


class Command(BaseCommand):
    help = 'Seed the database with sample restaurants near Acibadem University'

    def handle(self, *args, **options):
        loc, _ = Location.objects.get_or_create(city='Istanbul', district='Acibadem')

        category_names = {d['category'] for d in RESTAURANTS_DATA}
        categories = {}
        for name in category_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories[name] = cat

        created = 0
        for data in RESTAURANTS_DATA:
            if Restaurant.objects.filter(name=data['name']).exists():
                self.stdout.write(f'  SKIP (already exists): {data["name"]}')
                continue

            reviews = data.pop('reviews')
            category = categories[data.pop('category')]
            restaurant = Restaurant.objects.create(location=loc, category=category, **data)
            for author, rating, text in reviews:
                Review.objects.create(restaurant=restaurant, author=author, rating=rating, text=text)
            self.stdout.write(self.style.SUCCESS(f'  ADDED: {restaurant.name}'))
            created += 1

        self.stdout.write(self.style.SUCCESS(f'\nDone — {created} new restaurant(s) added.'))

        user_created = 0
        for u in USERS_DATA:
            if User.objects.filter(username=u['username']).exists():
                self.stdout.write(f'  SKIP (already exists): {u["username"]}')
                continue
            if u['is_superuser']:
                User.objects.create_superuser(u['username'], u['email'], u['password'])
            else:
                User.objects.create_user(u['username'], u['email'], u['password'])
            self.stdout.write(self.style.SUCCESS(f'  USER ADDED: {u["username"]}'))
            user_created += 1
        self.stdout.write(self.style.SUCCESS(f'Done — {user_created} new user(s) added.'))

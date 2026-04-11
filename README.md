# FlavorMap

A full-featured restaurant discovery web application built with Django, focused on the Acıbadem / Kadıköy district of Istanbul. Users can browse, search, and filter restaurants, read and write reviews, manage favorites, and explore menus — all in one place.

---

## Features

### Restaurant Discovery
- Browse restaurants with rich detail pages
- Search by name, description, or location
- Filter by category, price range, city, and minimum rating
- Sort by rating, popularity, or newest
- Embedded Google Maps for each restaurant

### Reviews & Community
- Star rating widget (1–5)
- Write reviews (one per user per restaurant)
- Like reviews
- Reply to reviews
- Review count and average rating displayed on listings

### User Accounts
- Registration and login
- Personal profile page with statistics (reviews written, favorites, owned restaurants)
- Favorites system (add/remove restaurants)

### Restaurant Management
- Owners can create, edit, and delete their restaurant listings
- Menu management (add/delete menu items by category)
- Photo gallery upload for restaurants

### Homepage
- Top-rated restaurants section
- New arrivals section
- Category browsing

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 4.2 |
| Database | SQLite (development) |
| Image Processing | Pillow |
| Frontend | HTML5, CSS3 (custom), Django Templates |

---

## Data Models

```
Category         — Restaurant categories (e.g. Turkish, Italian)
Location         — City / district info
Restaurant       — Core listing (name, description, address, photo, coordinates, price range)
MenuItem         — Menu items with price and availability, grouped by category
Review           — User reviews with star rating
ReviewReply      — Threaded replies on reviews
ReviewLike       — Like/unlike reviews (unique per user+review)
Favorite         — User's saved restaurants (unique per user+restaurant)
RestaurantPhoto  — Multiple photos per restaurant with captions
```

---

## Setup

### 1. Clone & create virtual environment

```bash
git clone https://github.com/sarginyaren/flavormap.git
cd flavormap
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Development mode | `True` |

### 3. Run migrations & seed data

```bash
python manage.py migrate
python manage.py seed_data    # loads sample restaurants, categories, and users
```

### 4. Start the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## Project Structure

```
flavormap/
├── flavor/                   # Django project config (settings, urls, wsgi)
├── restaurants/              # Main app
│   ├── models.py             # All data models
│   ├── views.py              # All view logic
│   ├── forms.py              # Django forms
│   ├── urls.py               # URL routing
│   ├── admin.py              # Admin panel config
│   └── management/
│       └── commands/
│           └── seed_data.py  # Sample data loader
├── templates/                # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── restaurants/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── form.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── static/css/               # Stylesheets
├── manage.py
├── requirements.txt
└── .env.example
```

---

## Screenshots

> Add screenshots here to showcase the homepage, restaurant detail page, and review system.

---

## License

This project is for educational purposes.

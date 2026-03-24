# flavor

A Django-based restaurant discovery app for the Acibadem / Kadikoy area in Istanbul. Browse, search and filter restaurants by category and price range, and read reviews.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development, `False` for production |

## Running

```bash
python manage.py migrate
python manage.py seed_data       # load sample restaurants
python manage.py runserver
```

## Tech stack

- Python 3.12
- Django 6.0
- SQLite (development)

# Sticky Notes Django App

## Setup
1. `pip install django`
2. `python manage.py migrate`
3. `python manage.py createsuperuser`
4. `python manage.py runserver`
5. Visit http://127.0.0.1:8000/notes/

## Features
- CRUD for notes with title/content.
- Bootstrap styling + custom CSS for sticky-note look.

## Notes
- No auth for simplicity.
- Static files: Run `collectstatic` for production.
# Sticky Notes Django App

A lightweight Django application for creating, viewing, editing, and deleting sticky notes. Built with class-based views, ModelForms, Bootstrap for responsive UI, and custom CSS for a "sticky" aesthetic. Includes unit tests for models, forms, and views.

## Demo
- Live: [Deploy if you want, e.g., on Heroku](https://your-deployed-url.com) (optional).
- Screenshots: Add images of the note list, form, etc.

## Features
- **CRUD Operations**: List, detail, create, update, delete notes.
- **Model**: Title (CharField), content (TextField), timestamps.
- **Styling**: Bootstrap + CSS (yellow sticky-note cards with hover effects).
- **Tests**: 100% coverage for key use cases (run `python manage.py test`).

## Quick Setup
1. Clone: `git clone https://github.com/yourusername/sticky-notes.git`
2. `pip install django`
3. `python manage.py migrate`
4. `python manage.py createsuperuser` (for admin)
5. `python manage.py runserver`
6. Visit `http://127.0.0.1:8000/notes/`

## Tech Stack
- Django 4+
- Bootstrap 5 (CDN)
- SQLite (dev)

## Tests
`python manage.py test notes` – All pass!

Built as part of my developer portfolio. Contributions welcome!
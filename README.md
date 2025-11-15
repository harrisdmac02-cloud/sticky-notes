# Sticky Notes Django App

## Overview
This is a simple CRUD app for managing sticky notes, built with Django. Users can create, view, edit, and delete notes with a clean, Bootstrap-styled interface. I designed it to practice models, views, forms, templates, and testing—key Django concepts.

## Features
- **Model**: Note with title (max 200 chars), content, and auto-timestamps.
- **Views**: Class-based generics for List, Detail, Create, Update, Delete.
- **Forms**: ModelForm with validation and Bootstrap styling.
- **Templates**: Extensible base.html with sticky-note CSS effects.
- **Tests**: Unit/integration tests covering models, forms, and views (run with `python manage.py test`).
- **Styling**: Bootstrap 5 CDN + custom CSS for a fun, rotatable card design.

## Setup Instructions
1. Clone the repo: `git clone <your-repo-url>`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Create superuser (optional): `python manage.py createsuperuser`.
5. Start server: `python manage.py runserver`.
6. Visit `http://127.0.0.1:8000/notes/` to add/view notes.

## Project Structure
sticky_notes/
├── manage.py
├── requirements.txt
├── README.md
├── sticky_notes/  # Project settings
├── notes/         # App: models, views, etc.
├── templates/     # HTML files
├── static/        # CSS
└── notes/tests.py # Tests


## Testing
- Run: `python manage.py test notes`.
- Covers: Model creation/str, form validation, view responses (GET/POST), edge cases (empty list, 404s).
- 100% coverage on core paths (verified manually).




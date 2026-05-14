# Home Organizer

A Django-based home management dashboard for tracking staff, salary, kitchen inventory, grocery, menu planning, tasks, and reminders.

## Features

- **Staff & Salary Management** — Add staff profiles, mark leaves, request advances, auto-generate salary with leave/advance deductions
- **Kitchen Management** — Pantry stock tracking, grocery lists with auto-compare (needed − at home = to buy), inventory logging, menu planning with step-by-step recipes
- **Task Checklists** — Assign recurring tasks (daily/weekly/monthly) to staff, track completion
- **Reminders** — Admin-managed reminders for subscriptions, maintenance, pest control, etc.
- **Notifications** — Bell icon with dropdown; alerts for task assignments, overdue tasks, salary due, leave/advance requests
- **Role-Based Access** — Admin sees everything; Cook sees menus/inventory; Marketer sees grocery/pantry; others see tasks/profile/salary
- **Authentication** — Staff accounts auto-created with manual username/password entry on staff creation
- **Premium UI** — Warm aesthetic with forest green/gold/cream palette, sidebar navigation, Prata + Nunito fonts

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Python 3.14 |
| Database | SQLite (dev), PostgreSQL (production) |
| Frontend | HTML, CSS, Bootstrap Icons, FullCalendar.js |
| Fonts | Google Fonts (Prata + Nunito) |

## Quick Start

```bash
# Clone and enter
git clone https://github.com/krishkrkashyap/Home-Organizer.git
cd Home-Organizer

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac

# Install dependencies
pip install django gunicorn psycopg2-binary

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Login with superuser credentials.

## Default Staff Login

When creating staff via `/staff/create/`, enter a username and password manually. Staff log in at the same login page and are redirected to their role-specific dashboard.

## Project Structure

```
Home-Organizer/
├── home_organizer/      # Project settings, URLs, root views
├── staff/               # Staff profiles, leaves, advances, salary
├── kitchen/             # Pantry, grocery, inventory, menu plans
├── tasks_app/           # Task templates, assignments, reminders
├── notifications/       # Notification system
├── templates/           # Base template, dashboard, login
├── static/              # CSS, JS, images
└── docs/                # Design specs and implementation plans
```

## Deploy to Render

### 1. Push to GitHub

```bash
git remote add origin https://github.com/krishkrkashyap/Home-Organizer.git
git push -u origin master
```

### 2. Render Configuration

**Web Service Settings:**
- **Runtime:** Python
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn home_organizer.wsgi`

**Environment Variables (add in Render dashboard):**
| Key | Value |
|-----|-------|
| `DJANGO_SETTINGS_MODULE` | `home_organizer.settings` |
| `DATABASE_URL` | (Render PostgreSQL URL — auto-provided if you add a PostgreSQL DB) |
| `SECRET_KEY` | (generate: `python -c "import secrets; print(secrets.token_urlsafe(50))"`) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |

### 3. PostgreSQL Database

Add a **PostgreSQL** database from Render dashboard. Render auto-sets the `DATABASE_URL` env var.

### 4. Production Settings

Create `home_organizer/settings_production.py` or use env vars to set:
- `DEBUG = False`
- `ALLOWED_HOSTS = ['.onrender.com']`
- Database from `DATABASE_URL` (dj-database-url)
- `STATIC_ROOT` + `STATICFILES_STORAGE` for static files
- `CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']`

Then run:
```bash
python manage.py collectstatic
python manage.py migrate
```

---

Built with Django — because a well-organized home runs on clean data.

# Gazelle

A basic Django hiring platform for adding and tracking candidates. Backed by PostgreSQL, styled in white, black and marigold.

## Features

- **Create** – add a candidate (name, email, phone, position, status, LinkedIn, resume link, notes)
- **Read** – list view with search and status filter, plus a detail page
- **Update** – edit any candidate
- **Delete** – with a confirmation page
- Django admin registered at `/admin/`

## Quick start

```bash
# 1. Start Postgres (or point the POSTGRES_* env vars at your own instance)
docker compose up -d

# 2. Python env
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Database
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin

# 4. Run
python manage.py runserver
```

Open http://127.0.0.1:8000 — it redirects to `/candidates/`.

The defaults in `settings.py` match `docker-compose.yml`, so no env setup is needed for local dev. To override, export the variables in `.env.example` (e.g. `set -a; source .env; set +a`).

## Tests

```bash
python manage.py test candidates
```

## Project layout

```
gazelle/                 project settings & root urls
candidates/
  models.py              Candidate model + Status choices
  forms.py               CandidateForm (ModelForm)
  views.py               List/Detail/Create/Update/Delete class-based views
  urls.py                /candidates/, /new/, /<pk>/, /<pk>/edit/, /<pk>/delete/
  templates/candidates/  page templates
templates/base.html      shared layout
static/css/styles.css    theme (colors live in :root variables)
```

## Extending

- New fields: add to `Candidate`, then `python manage.py makemigrations && python manage.py migrate`, and add to `CandidateForm.Meta.fields`.
- Pipeline stages: edit `Candidate.Status` and add a matching `.badge-<value>` style in `styles.css`.
- Theme colors: change `--gold`, `--black`, etc. at the top of `styles.css`.

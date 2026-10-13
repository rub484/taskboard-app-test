# Taskboard

A small example app: **Django 5 + HTMX + Tailwind CSS v4 + PostgreSQL**, running in Docker.

Add tasks, tick them off, delete them — every action is an HTMX request that swaps
a single HTML fragment, no page reloads and no custom JavaScript.

## Run it

```bash
cp .env.example .env
docker compose up --build
```

Open http://localhost:8000. Three containers start:

| Service    | What it does                                       |
|------------|----------------------------------------------------|
| `db`       | PostgreSQL 17 (data kept in the `pgdata` volume)   |
| `web`      | Django dev server, runs migrations on start        |
| `tailwind` | Watches templates and rebuilds `static/css/app.css`|

Code is mounted into the containers, so edits to Python and templates reload live.

### Useful commands

```bash
docker compose exec web python manage.py createsuperuser   # then visit /admin
docker compose exec web python manage.py test
docker compose exec db psql -U taskboard                    # poke at the database
```

## Layout

```
config/            Django settings, urls, wsgi
tasks/             the app: model, views, urls, tests
templates/         base layout, page and the _task.html row partial
static/src/        Tailwind input
Dockerfile         node stage builds CSS, python stage runs gunicorn
docker-compose.yml db + web + tailwind watcher
```

## How the HTMX bits work

- **Add**: the form posts to `/tasks/`, the view returns one `<li>`, and HTMX inserts it at the top of the list.
- **Toggle**: posts to `/tasks/<id>/toggle/`, the returned `<li>` replaces the old one.
- **Delete**: sends `DELETE /tasks/<id>/`, the empty response replaces the row.

The CSRF token is sent on every HTMX request through `hx-headers` on `<body>`.

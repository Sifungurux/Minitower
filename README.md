# Minitower

Django 4.2 LTS app for tracking hosts, inventory, and firewall rules.

## Local setup (venv)

Requires Python 3.9–3.11 (Django 4.2's supported range — a much newer system
`python3` may not work cleanly). If your default `python3` is newer, point
the venv at a compatible interpreter instead (e.g. via `pyenv` or Homebrew's
`python@3.11`).

1. **Create and activate a virtualenv** in the repo root:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r test/requirements.txt
   ```

3. **Create the env file** at `minitower/.env` (this exact path — `django-environ`
   resolves it relative to `settings.py`, not the repo root). At minimum:

   ```bash
   cat > minitower/.env <<'EOF'
   SECRET_KEY=change-me
   DATABASE=sqlite3
   EOF
   ```

   `DATABASE` is required — `settings.py` reads it with no default and will
   raise on startup without it. `sqlite3` needs no other config; any other
   value switches to PostgreSQL and requires `DATABASE_NAME`, `DATABASE_USER`,
   `DATABASE_PASSWORD`, `DATABASE_HOST`, and `DATABASE_PORT` as well. For a
   real `SECRET_KEY`, generate one once dependencies are installed:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **Run migrations and start the dev server:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/`. Optionally create an admin user with
   `python manage.py createsuperuser`.

## Running tests

```bash
pytest
```

Settings for test runs come from `pytest.ini` (`DJANGO_SETTINGS_MODULE = minitower.settings`).
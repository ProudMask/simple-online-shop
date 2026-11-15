# Simple Online Shop

A local Flask/SQLite account and product-catalog demo. Register an account, log in, view a protected dashboard, and browse synthetic abaya products. There is no cart, ordering, or payment processing.

## Run locally

Python 3.10 or later:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app seed-demo
flask --app app run
```

Open http://127.0.0.1:5000. Demo seeding creates two synthetic products, is repeatable, and creates no accounts. Register your own local demo account using a password of 12–128 characters. To create empty tables instead, use `flask --app app init-db`.

SQLite defaults to `instance/shop_demo.sqlite3`. This new database name intentionally avoids silently reusing the original prototype's schema. Existing databases require an explicit migration before reuse; create_all does not migrate tables. Back up any existing data. Prices are fixed-point decimal values, displayed as AED for the demo.

## Configuration and structure

`SECRET_KEY` may be set in the environment to preserve sessions across restarts. Otherwise a new random key is generated at startup. `DATABASE_URL` optionally overrides the SQLAlchemy URL. No secrets are embedded in source. Debug mode is off by default.

- `app.py`: application factory, blueprint registration, form-token checks, initialization commands.
- `models.py`: product/category/user models.
- `auth.py`: registration, password verification, login/logout, protected dashboard.
- `views.py`: catalog route.
- Root HTML files: intentionally configured as the Jinja template directory.

Passwords use Werkzeug password hashes. Session state is cleared on login/logout, changes use POST with session-bound form tokens, and database queries use SQLAlchemy. Email addresses are trimmed and case-normalized; the demo checks syntax but does not verify ownership. Never use real credentials for a portfolio demonstration.

## Verify

```bash
python -m unittest discover -s tests -v
```

Tests use an isolated in-memory database and cover registration, hashing, duplicate accounts, invalid credentials, protected access, logout, CSRF rejection, catalog rendering, and repeatable seeding.

## Scope

This is a local educational prototype, not a production commerce/authentication system. It lacks email verification, password recovery, rate limiting, multi-factor authentication, audit logging, and deployment configuration. Do not expose the development server publicly. No mail is sent or purchase executed. This demonstrates application integration and account fundamentals, not statistical modeling or ML.

# COUNTY_PORTAL1

## Overview

COUNTY_PORTAL1 is a modern, role-based Flask web application for managing county government services, user accounts, and permit workflows. It supports multiple user roles (Super Admin, Staff, Citizen, Guest), secure authentication, permit application/review, and administrative dashboards.

### Key Features
- User authentication and registration (Flask-Security)
- Role-based dashboards (Super Admin, Staff, Citizen, Guest)
- Permit application, review, and document upload
- County, department, and user management
- Email notifications (Flask-Mail, Gmail SMTP)
- CSRF protection and secure password hashing (bcrypt)
- Semantic search-ready codebase and modular structure

## Project Structure

- `app/` - Main application package
  - `main/` - Views and routes for dashboards and main pages
  - `auth/` - Authentication and user profile management
  - `api/` - API endpoints (if any)
  - `models/` - SQLAlchemy models (User, County, Permit, etc.)
  - `forms.py` - WTForms classes for user and permit forms
  - `extensions.py` - Flask extension instances
  - `utils/` - Constants and helpers
- `config.py` - Configuration (reads from environment, safe defaults for dev)
- `run.py` / `wsgi.py` - App entry points
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Setup & Security

- **SECRET_KEY is required for production!**
  - Set the `SECRET_KEY` environment variable in your Render dashboard or production environment.
  - If not set, a default (insecure) key will be used for development only.
- Optionally, set `WTF_CSRF_SECRET_KEY` for extra CSRF protection. If not set, it will use `SECRET_KEY`.
- Example `.env` for local development:
  ```env
  SECRET_KEY=your-very-secret-key
  SECURITY_PASSWORD_SALT=your-password-salt
  DATABASE_URL=postgresql://user:password@localhost:5432/dbname
  MAIL_USERNAME=your@email.com
  MAIL_PASSWORD=your-app-password
  MAIL_DEFAULT_SENDER=your@email.com
  ```

## Deployment Notes
- On Render or any production host, always set `SECRET_KEY` and `SECURITY_PASSWORD_SALT` as environment variables.
- Never commit production secrets to version control.
- For Docker Compose, ensure your database service is named `db` or update the host in your `.env`.

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your values (or set env vars directly).
3. Run locally: `python run.py`

## Semantic Search & Codebase Navigation

This project is structured for easy semantic search and code navigation:
- Models, forms, and routes are modular and well-named.
- All configuration is centralized in `config.py`.
- Use semantic search tools to quickly find models, routes, or utility functions by name or docstring.

## License

This project is for demonstration and educational purposes. Please review and adapt for your own use case and security requirements.

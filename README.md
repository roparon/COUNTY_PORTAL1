# COUNTY_PORTAL1

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

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your values (or set env vars directly).
3. Run locally: `python run.py`

---

For more details, see the code comments in `config.py`.

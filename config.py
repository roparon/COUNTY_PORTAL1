import os
from dotenv import load_dotenv

# Load environment variables from a .env file (useful for local dev)
load_dotenv()

class Config:
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or \
        f"postgresql://{os.getenv('POSTGRES_USER', 'devuser')}:" \
        f"{os.getenv('POSTGRES_PASSWORD', 'devpass')}@" \
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:" \
        f"{os.getenv('POSTGRES_PORT', '5432')}/" \
        f"{os.getenv('POSTGRES_DB', 'county')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security keys
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'dev-password-salt-change-me')
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', SECRET_KEY)

    # Flask-Security settings
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_CONFIRMABLE = False
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_SEND_PASSWORD_RESET_EMAIL = True   # Password reset instructions      
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True  # Password change notifications
    SECURITY_EMAIL_HTML = True                  # Send HTML emails                 
    SECURITY_EMAIL_PLAINTEXT = True             # Send plain text emails

    # Custom email subjects
    SECURITY_EMAIL_SUBJECT_REGISTER = "Welcome to County Services Portal"
    SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = "Password Reset Instructions"
    SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = "Password Changed Successfully"

    # Flask-Mail settings (default to Gmail SMTP)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes', 'on')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes', 'on')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Gmail address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Gmail app password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

import os
from dotenv import load_dotenv
from passlib.hash import bcrypt
hashed = bcrypt.hash("my_secure_password")
print(bcrypt.verify("my_secure_password", hashed))


load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db') or \
        f"postgresql://{os.getenv('POSTGRES_USER', 'devuser')}:{os.getenv('POSTGRES_PASSWORD')}@" \
        f"{os.getenv('POSTGRES_HOST', 'db')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'county')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    #flask-security settings
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_PASSWORD_HASH = 'bcrypt'  #use bcrypt for password hashing over argon2
    SECURITY_CONFIRMABLE = False
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False        # Registration confirmation        
    SECURITY_SEND_PASSWORD_RESET_EMAIL = True  # Password reset instructions      
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True # Password change notifications
    # Email templates and customization                                           
    SECURITY_EMAIL_HTML = True                 # Send HTML emails                 
    SECURITY_EMAIL_PLAINTEXT = True           # Send plain text emails

    # Email subjects (customizable)                                               
    SECURITY_EMAIL_SUBJECT_REGISTER = "Welcome to County Services Portal"         
    SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = "Password Reset Instructions"         
    SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = "Password Changed Successfully"

    # Flask-Mail Settings (Gmail SMTP)                                        
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')             
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))                         
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes', 'on')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes', 'on')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Your Gmail address     
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Your Gmail app password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
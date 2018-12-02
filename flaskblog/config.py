"""
App Configuration
    Config class
"""
import os

# Specifiy default values

"""
Imports:
    os: get environment variables
"""

class Config:
    """Config class
    Handles different configs for prod/dev sites
    """

    # secret key protects against XSS and modifying cookies
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    # dev db sqlite, site db will be created in project-root
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_SQLALCHEMY_DATABASE_URI')
    # email settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # get env-vars
    MAIL_USERNAME = os.environ.get('FLASK_EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('FLASK_EMAIL_PW')
    MAIL_SENDER = os.environ.get('FLASK_EMAIL_SENDER')

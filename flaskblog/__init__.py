"""
Initialize app
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
"""
Imports:
    os, read env-vars
    Flask:
        Flask
    flask_sqlalchemy, ORM to handle db
    flask_bcrypt, pw encryption
    flask_login, handle logins, user auth etc
    flask_mail, send emails
"""

# the webapp
app = Flask(__name__)
# todo: handle diff configs for prod/dev sites
# secret key protects against XSS and modifying cookies
app.config['SECRET_KEY'] = '1f42b9684a5a4a362d03e287301d2ac2b2a9765ab062b5fa'
# dev db sqlite, site db will be created in project-root
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# create db instance:
db = SQLAlchemy(app)
# create bcrypt instance
bcrypt_flask = Bcrypt(app)
# create login-manager instance
login_mgmr = LoginManager(app)
# tell the login extension where the login route is located
# pass the function name of the login route (same as we pass in with the url_for)
login_mgmr.login_view = 'login'
# enable bootstrap
login_mgmr.login_message_category = 'info'
# email settings
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# get env-vars
app.config['MAIL_USERNAME'] = os.environ.get('FLASK_EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('FLASK_EMAIL_PW')
# initialize mail extension
mail = Mail(app)

# after db create etc since routes uses db etc
from flaskblog import routes
"""
Imports:
    flaskblog:
        routes
"""

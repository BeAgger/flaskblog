"""
Initialize app
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

"""
Imports:
    Flask:
        Flask
    flask_sqlalchemy, ORM to handle db
    flask_bcrypt, pw encryption
    flask_login, handle logins, user auth etc
    flask_mail, send emails
    flaskblog: config
"""

# Initialize extentions without assigning to the app-var,
# so the extention-object is not initially bound to the app.
# No app specific state wil then be stored on the extension object,
# that can be used in multiple apps

# create db instance:
db = SQLAlchemy()
# create bcrypt instance
bcrypt_flask = Bcrypt()
# create login-manager instance
login_mgmr = LoginManager()
# tell the login extension where the login route is located
# pass the function name of the login route (same as we pass in with the url_for)
login_mgmr.login_view = 'users.login'
# enable bootstrap
login_mgmr.login_message_category = 'info'
# initialize mail extension
mail = Mail()

# after db create etc since routes uses db etc
...


# App factory function
def create_app(config_class=Config):
    """
    App factory function
    Args: Configuration object for our app, ie dev, prod etc.
    Imports:
        flaskblog:
            users.routes: user blueprint
            posts.routes: post blueprint
            main.routes: main blueprint
    """
    # configuration via Config
    # init the webapp
    app = Flask(__name__)
    app.config.from_object(Config)

    # import user routes from user module
    # users = users variable in users/routes.py instantiatiated by Blueprint()
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main

    # register the routes to the app
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    # Initialize extension to app
    db.init_app(app)
    bcrypt_flask.init_app(app)
    login_mgmr.init_app(app)
    mail.init_app(app)

    return app

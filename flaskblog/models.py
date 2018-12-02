"""
Entity models
"""
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_mgmr, app
from flask_login import UserMixin
"""
Imports:
    Python:
        datetime to post default date
        itsdangerous to handle tokens used in mail. Used i User.
    flaskblog:
        db (database created in flaskblog.py)
        login_manager to handle logged in users, def load_user
        app to get the secret key, used in User
    flask_login:
        UserMixin to add required attributes and functions, inherited in User class
"""

# decorate so LoginManager extension knows this is the function that gets the user by id
@login_mgmr.user_loader
def load_user(user_id):
    """Get user by id"""
    return User.query.get(int(user_id))


# Create db model classes
class User(db.Model, UserMixin):
    """
    User entity class
        id, username, email, image_file, password, posts-relation
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """get_reset_token"""
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # decorator to tell py not to expect the self parameter as an argument
    @staticmethod
    def verify_reset_token(token):
        """verify_reset_token"""
        s = Serializer(app.config['SECRET_KEY'])
        # handle SignatureExpired exeption
        try:
            user_id = s.loads(token)['user_id']
        except:
            # Do nothing
            return None
        # return the user with the user_id from the token payload
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """
    Post entity class
        id, title, data_posted, content, user_id
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



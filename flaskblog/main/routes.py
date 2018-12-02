"""
Main.routes
    home(): /, /home
    about(): /about
"""

from flask import render_template, request, Blueprint
from flaskblog.models import Post

"""
Imports:
    Flask
        Blueprints to modularize the webapp
        render_template to render the html form (ie. home.html, about.html...)
        request to GET http arguments
    flaskblog.models:
        User and Post entity class

"""

# Instantiate main blueprint
main = Blueprint('main', __name__)

# Create routes specifically to the main module and register in #


@main.route("/")
@main.route("/home")
def home():
    """Home route and render form"""
    # set the page from GET, default 1, must be int else page throws valueerror!
    page = request.args.get('page', 1, type=int)
    # get 5 posts from db
    # order by newest post
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/home")
def latest_posts():
    """Home route and render form"""
    # set the page from GET, default 1, must be int else page throws valueerror!
    page = request.args.get('page', 1, type=int)
    # get 5 posts from db
    # order by newest post
    # query.(Model).filter(something).limit(5).all()
    posts = Post.query\
        .order_by(Post.date_posted.desc())\
        .limit(2)\
        .paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    """About route and render form"""
    return render_template('about.html', title='About')



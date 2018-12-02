"""
Routes
"""
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt_flask, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                            PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
"""
Imports:
    os: used in save_picture
    secrets: used in save_picture
    PIL (Pillow): used in save_picture(), resize image
    Flask:
        render_template to render the html form (ie. home.html, about.html...)
        url_for to manage links properly
        flash to show messages to user
        redirect to redirect between forms and pages
        abort to handle abortion of code execution, used in update_post()
    flaskblog:
        app, db, bcrypt_flask, mail
    flaskblog.forms:
        user-defined forms: register, login, updateaccount, posts, reset password forms
    flaskblog.models:
        User and Post entity class
    flask_login:
        login_user function used in login route
        current_user: register and login to vheck for a logged in user
        logout_user logout user out used in logout route
        login_required decorator to routes that needs user is logged in
    flask_mail: Message, used in send_mail, to send emails
"""


@app.route("/")
@app.route("/home")
def home():
    """Home route and render form"""
    # set the page from GET, default 1, must be int else page throws valueerror!
    page = request.args.get('page', 1, type=int)
    # get 5 posts from db
    # order by newest post
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    """About route and render form"""
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
# must accept both get and post requests.
def register():
    """Register route and render form. Validate user."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    # check if form validated properly (when we come back to the form after submit)
    if form.validate_on_submit():
        # if validate ok, show message to user. use bootstrap alert style class: success
        # Create account:
        #  hash the pw
        hsh_pw = bcrypt_flask.generate_password_hash(form.password.data, 12).decode('utf-8')
        # create user with form-data
        user = User(username=form.username.data, email=form.email.data, password=hsh_pw)
        db.session.add(user)
        db.session.commit()
        # We're ok:
        flash('Account created. Please login.', 'success')
        # redirect to home page
        return redirect(url_for('login'))
    # if no validate render form
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login route and render form. Login user."""
    # If user is already logged in send to home
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt_flask.check_password_hash(user.password, form.password.data):
            # if user exists and password is validated
            login_user(user, remember=form.remember.data)
            # get next parameter if it exists
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            # flash('You have been logged in', 'success')
        else:
            flash('Access denied. Login failed!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    """Log the user out"""
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    """Save the picture"""
    # Randomize the filename to avoid filename collision
    random_hex = secrets.token_hex(8)
    # get extension
    _, f_ext = os.path.splitext(form_picture.filename)
    # construct picture name and path
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # resize image with Pillow image module
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    # save resized image
    img.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """Account"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # check if theres picture data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # update currentuser with new image
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # populate fields if GET
        form.username.data = current_user.username
        form.email.data = current_user.email

    # get users imagefile from db and load it
    image_file = url_for('static',
                         filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """Create new post"""
    form = PostForm()
    if form.validate_on_submit():
        post_new = Post(title=form.title.data, content=form.content.data, author=current_user)
        # set the author by using the backref author in stead of user_id
        db.session.add(post_new)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title="New Post",
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    """Show a post"""
    post_cur = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post_cur.title, post=post_cur)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """Update a post"""
    post_upd = Post.query.get_or_404(post_id)
    # only allow edit if current user is the author
    if post_upd.author != current_user:
        abort(403)
    form = PostForm()
    # add to db if form submitted successfully
    if form.validate_on_submit():
        post_upd.title = form.title.data
        post_upd.content = form.content.data
        db.session.add(post_upd)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('post', post_id=post_upd.id))
    elif request.method == 'GET':
        # else populate with current post data
        form.title.data = post_upd.title
        form.content.data = post_upd.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post"""
    post_del = Post.query.get_or_404(post_id)
    if post_del.author != current_user:
        abort(403)
    db.session.delete(post_del)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    """User route and render form"""
    # set the page from GET, default 1, must be int else page throws valueerror!
    page = request.args.get('page', 1, type=int)
    # get user
    user = User.query.filter_by(username=username).first_or_404()
    # get 5 posts from user from db
    # order by newest post
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route("/home")
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


def send_reset_email(user):
    """send email to user with reset token"""
    # get token:
    token = user.get_reset_token()
    # Message(title, sender,
    msg = Message('Password reset request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    # Jinja2 template to nicer mail
    msg.body = f'''
To reset your password, click this link: {url_for('reset_token', token=token, _external=True)}

If you did not request this, just ignore this email!
'''
    # mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """Request password reset"""
    # The user must be logged out to get to the form
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    # since forms will return to forms they're sent from we add submet-validation here
    if form.validate_on_submit():
        # get the user
        user = User.query.filter_by(email=form.email.data).first()
        # send email to user
        send_reset_email(user)
        flash('An email has been sent with reset instructions.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Request password reset"""
    # is token active? get from url
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    # If no user, token invalid or expired
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hsh_pw = bcrypt_flask.generate_password_hash(form.password.data, 12).decode('utf-8')
        user.password = hsh_pw
        db.session.commit()
        flash('Password updated. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

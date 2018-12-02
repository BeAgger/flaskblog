"""
Posts.routes
    new_post(): /post/new
    post(post_id): /post/<int:post_id>
    update_post(post_id): /post/<int:post_id>/update
    delete_post(post_id): /post/<int:post_id>/delete
"""

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

"""
Imports:
    Flask
        Blueprints
        render_template to render the html form (ie. home.html, about.html...)
        url_for to manage links properly
        flash to show messages to user
        redirect to redirect between forms and pages
        request to GET http arguments
        abort to handle abortion of code execution, used in update_post()
    flask_login:
        current_user: register and login to vheck for a logged in user
        login_required decorator to routes that needs user is logged in
    flaskblog:
        db
    flaskblog.models:
        Post entity class
    flaskblog.posts.forms:
        user-defined forms: posts forms
"""

# Instantiate posts blueprint
posts = Blueprint('posts', __name__)

# Create routes specifically to the posts module and register in #

@posts.route("/post/new", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title="New Post",
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    """Show a post"""
    post_cur = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post_cur.title, post=post_cur)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post_upd.id))
    elif request.method == 'GET':
        # else populate with current post data
        form.title.data = post_upd.title
        form.content.data = post_upd.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post"""
    post_del = Post.query.get_or_404(post_id)
    if post_del.author != current_user:
        abort(403)
    db.session.delete(post_del)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('main.home'))

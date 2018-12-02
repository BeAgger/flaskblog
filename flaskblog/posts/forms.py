"""
Posts.forms:
    PostForm(FlaskForm)
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


"""
Imports:
    Flask
        Blueprints

"""

# Create forms specifically to the posts module

class PostForm(FlaskForm):
    """Show posts"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post it')

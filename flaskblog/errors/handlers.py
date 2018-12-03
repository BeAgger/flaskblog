"""
Error handlers
Imports:
    Blueprint

"""
from flask import Blueprint, render_template

# Instantiate
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(403)
def error_403(error):
    """403 Errors"""
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(404)
def error_404(error):
    """404 Errors"""
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def error_500(error):
    """500 Errors"""
    return render_template('errors/500.html'), 500

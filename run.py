"""
Main application
"""
from flaskblog import create_app

# create app from factory function
# pass in configs, no args use default
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

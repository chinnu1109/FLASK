# Blueprint is used to organize a Flask application into small, manageable parts instead of writing everything in one file.
# Blueprint helps to:
# Separate routes
# Separate logic
# Reuse code
# Work in teams

# url_prefix='/auth' is used to add a prefix to all routes in the blueprint

from flask import Flask
from auth import auth_bp
# Bring that box of routes from auth.py”

app = Flask(__name__)

# Attach blueprint to app
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return "This is Home Page"

if __name__ == '__main__':
    app.run(debug=True)

# auth.py creates routes
# app.py activates those routes

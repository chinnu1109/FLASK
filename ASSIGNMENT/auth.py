from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
# “I am creating a box named auth_bp”
# This box will store routes


@auth_bp.route('/login')
def login():
    return "This is Login Page"

@auth_bp.route('/register')
def register():
    return "This is Register Page"

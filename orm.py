from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# Creates a Flask application
# __name__ tells Flask where the app is located
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
print("DB will be created at:", os.path.abspath("demo.db"))
# ---------- USER TABLE ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    skills = db.Column(db.String(20))
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete")

# ---------- POST TABLE ----------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- ROUTES ----------
@app.route('/')
def index():
    users = User.query.all()
    posts = Post.query.all()
    return render_template('index1.html', users=users, posts=posts)

@app.route('/add_user', methods=['POST'])
def add_user():
    user = User(
        username=request.form['username'],
        email=request.form['email'],
        phone_number=request.form.get('phone_number'),
        gender=request.form.get('gender'),
        skills=request.form.get('skills')
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_post', methods=['POST'])
def add_post():
    post = Post(
        title=request.form['title'],
        content=request.form['content'],
        author_id=request.form['author_id']
    )
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        user.phone_number = request.form.get('phone_number', user.phone_number)
        user.gender = request.form.get('gender', user.gender)
        user.skills = request.form.get('skills', user.skills)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_user.html', user=user)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/delete_user/<int:id>', methods=['DELETE'])
def delete_user_api(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return {
        "message": "User deleted successfully",
        "user_id": id
    }, 200

if __name__ == '__main__':
    app.run(debug=True)


# app = Flask(__name__)
# app.config['secret key'] = 'secret-key'
# app.config[] 
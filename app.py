from flask import Flask, flash, redirect, render_template, request, session, current_app
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import HTTPException, NotFound
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import aliased
import sqlite3
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

Session(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please login to access this page.'

class User(UserMixin):
    def __init__(self, id, username, email, password, authenticated):
         self.id = id
         self.username = username
         self.email = email
         self.password = password
         self.authenticated = authenticated
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id


def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', user_id).fetchone()
    conn.close()
    if user:
        return User(*tuple(user))
    return None


@app.before_request
def before_request():
    if not getattr(current_app, "user_loaded", False) and "user" in session:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (session["user"]["email"],)).fetchone()
        conn.close()
        
        if user:
            login_user(User(*tuple(user)))
            current_app.user_loaded = True


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password = str(password)

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = (?)", (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user["password_hash"], password):
            session['user'] = {"email": user["email"], "username": user["username"]}
            return redirect("/")
        else:
            flash('Login Unsuccessful. Please check email and password',
                  category='danger')

    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password = str(password)
        confirm = request.form.get('confirm')
        confirm = str(confirm)

        if not (username and email and password and confirm):
            flash("All fields are required.")
            return redirect("/register")

        if password != confirm:
            flash("Passwords don't match. Please try again.")
            return redirect("/register")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = (?)", (email,)).fetchone()
        conn.close()

        if user:
            flash('Email already exists. Please try again.', category='danger')
        else:
            password_hash = generate_password_hash(password)
            conn = get_db_connection()
            conn.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))
            conn.commit()
            conn.close()
            flash('Account created successfully. Please login.', category='success')
            return redirect("/login")
        
    return render_template('register.html')


@app.errorhandler(Exception)
def error(e):
    print(e)
    if isinstance(e, HTTPException):
        return render_template('error.html', code=e.code, description=e.description)
    
    return render_template('error.html', code="500", description="Internal Server Error")

from flask import Flask, flash, redirect, render_template, request, session, current_app
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import HTTPException
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import sqlite3

def split_string(value, sep):
    return value.split(sep)

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.jinja_env.filters['split'] = split_string

Session(app)
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
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
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
            next_url = request.args.get('next')
            if not next_url:
                next_url = '/notes'
            return redirect(next_url)
        else:
            flash('Login Unsuccessful. Please check email and password', category='danger')

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


@app.route('/notes', methods=["GET"])
@login_required
def notes():
    conn = get_db_connection()
    notes = conn.execute("""
    SELECT n.*, GROUP_CONCAT(DISTINCT l.label_name) AS labels 
    FROM notes n 
    LEFT JOIN notes_labels nl ON n.id = nl.note_id 
    LEFT JOIN labels l ON nl.label_id = l.id
    WHERE n.user_id = ? 
    GROUP BY n.id
    """, (current_user.id,)).fetchall()
    labels = conn.execute("SELECT * FROM labels WHERE user_id = (?)", (current_user.id,)).fetchall()
    conn.close()
    return render_template('notes.html', notes=notes, labels=labels)


@app.route('/notes/new', methods=["POST"])
@login_required
def new_note():
    title = request.form.get('title')
    content = request.form.get('content')
    labels = request.form.getlist('multiLabels')

    if not title:
        flash("Title is required.", category='warning')
        return redirect("/notes")

    conn = get_db_connection()
    temp = conn.execute("INSERT INTO notes (title, note_content, user_id) VALUES (?, ?, ?)", (title, content, current_user.id))
    conn.commit()
    print(temp)
    note = conn.execute("SELECT * FROM notes WHERE title = (?) AND note_content = (?) AND user_id = (?)", (title, content, current_user.id)).fetchone()
    note_id = note["id"]
    for label in labels:
        conn.execute("INSERT INTO notes_labels (note_id, label_id) VALUES (?, ?)", (note_id, label))
    conn.commit()
    conn.close()
    flash('Note created successfully.', category='success')
    return redirect("/notes")


@app.route('/notes/<int:id>/edit', methods=["GET", "POST"])
@login_required
def edit(id):
    conn = get_db_connection()
    note = conn.execute("SELECT * FROM notes WHERE id = (?) AND user_id = (?)", (id, current_user.id)).fetchone()
    labels = conn.execute("SELECT * FROM labels WHERE user_id = (?)", (current_user.id,)).fetchall()
    note_labels = conn.execute("SELECT nl.label_id AS label FROM notes n JOIN notes_labels nl ON n.id = nl.note_id WHERE n.user_id = ? AND n.id = ?", (current_user.id, id)).fetchall()
    conn.close()

    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        labels = request.form.getlist('multiLabels')

        if not title:
            flash("Title is required.")
            return redirect("/notes/" + str(id) + "/edit")

        conn = get_db_connection()
        conn.execute("DELETE FROM notes_labels WHERE note_id = (?)", (id, ))
        conn.execute("UPDATE notes SET title = (?), note_content = (?) WHERE id = (?) AND user_id = (?)", (title, content, id, current_user.id))
        conn.commit()
        for label in labels:
            conn.execute("INSERT INTO notes_labels (note_id, label_id) VALUES (?, ?)", (id, label))
        conn.commit()
        conn.close()
        flash('Note updated successfully.', category='success')
        return redirect("/notes")
    
    return render_template('editNote.html', note=note, labels=labels, note_labels=[label["label"] for label in note_labels])


@app.route('/notes/<int:id>/delete', methods=["GET"])
@login_required
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM notes_labels WHERE note_id = (?)", (id, ))
    conn.execute("DELETE FROM notes WHERE id = (?) AND user_id = (?)", (id, current_user.id))
    conn.commit()
    conn.close()
    flash('Note deleted successfully.', category='success')
    return redirect("/notes")


@app.route('/notes/labels/<int:id>', methods=["GET"])
@login_required
def labeled_notes(id):
    conn = get_db_connection()
    notes = conn.execute("""
        SELECT n.*, GROUP_CONCAT(DISTINCT l.label_name) AS labels 
        FROM notes n 
        LEFT JOIN notes_labels nl ON n.id = nl.note_id 
        LEFT JOIN labels l ON nl.label_id = l.id
        WHERE n.user_id = ? AND nl.label_id = ?
        GROUP BY n.id
    """, (current_user.id, id)).fetchall()
    labels = conn.execute("SELECT * FROM labels WHERE user_id = (?)", (current_user.id,)).fetchall()
    conn.close()
    return render_template('notes.html', notes=notes, labels=labels)


@app.route('/labels/add', methods=["GET", "POST"])
@login_required
def add_label():
    if request.method == "POST":
        label = request.form.get('labelInput')
        if not label:
            flash("Label name is required.")
            return redirect("/notes")
        conn = get_db_connection()
        if conn.execute("SELECT * FROM labels WHERE label_name = ? and user_id = ?", (label, current_user.id)).fetchall():
            flash("Label already exists.")
            return redirect("/notes")
        conn.execute("INSERT INTO labels (label_name, user_id) VALUES (?, ?)", (label, current_user.id))
        conn.commit()
        conn.close()
        flash('Label added successfully.', category='success')
        return redirect("/notes")
    return redirect("/notes")


@app.route('/labels/<int:id>/delete', methods=["GET", "POST"])
@login_required
def delete_label(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM notes_labels WHERE label_id = (?)", (id, ))
    conn.execute("DELETE FROM labels WHERE id = (?) AND user_id = (?)", (id, current_user.id))
    conn.commit()
    conn.close()
    flash('Label deleted successfully.', category='success')
    return redirect("/notes")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    current_app.user_loaded = False
    return redirect("/")


@app.errorhandler(Exception)
def error(e):
    print(e)
    if isinstance(e, HTTPException):
        return render_template('error.html', code=e.code, description=e.description)
    
    return render_template('error.html', code="500", description="Internal Server Error")

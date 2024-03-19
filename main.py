from flask import Flask, render_template, request, url_for, flash, redirect, abort, g
from flask_bcrypt import generate_password_hash, check_password_hash
import sqlite3
import atexit
from dotenv import load_dotenv
from flask_login import current_user, LoginManager, UserMixin, login_user, logout_user
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('app_key')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['password'])
    else:
        return None
    
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['id'], user_data['username'], user_data['password'])
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()

            flash('User registered successfully!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)

@app.route('/network_notes')
def network_notes():
    return render_template('network_notes.html')

@app.route('/infastructure_notes')
def infrastructure_notes():
    return render_template('infrastructure_notes.html')

@app.route('/create', methods=('GET', 'POST'))
def create():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.username != 'admin':
        abort(403)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('A post title is required!')
        elif not content:
            flash('Some content for the post is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('posts'))

    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.username != 'admin':
        abort(403)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('A post title is required!')
        
        elif not content:
            flash('Some content for the post is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('posts'))
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.username != 'admin':
        abort(403)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted from the posts!'.format(post['title']))
    return redirect(url_for('posts'))

if __name__ == "__main__":
    app.run(debug=True)
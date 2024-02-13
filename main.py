from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ea579ce9def1ffca2d3dfd78a6aa9c9760b270950268405b'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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

@app.route('/create')
def create():
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
app.run(debug=True)
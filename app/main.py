
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from app import get_db_connection
from app.models import User

main = Blueprint('main', __name__)


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/projects')
def projects():
    return render_template('projects.html')


@main.route('/posts', methods=['GET', 'POST'])
def posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)


@main.route('/network_notes')
def network_notes():
    return render_template('network_notes.html')


@main.route('/infrastructure_notes')
def infrastructure_notes():
    return render_template('infrastructure_notes.html')


@main.route('/create', methods=['GET', 'POST'])
def create():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
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
            conn.execute(
                'INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('main.posts'))

    return render_template('create.html')


@main.route('/<int:id>/edit/', methods=['GET', 'POST'])
def edit(id):
    post = get_post(id)
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
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
            conn.execute(
                'UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('main.posts'))

    return render_template('edit.html', post=post)


@ main.route('/<int:id>/delete/', methods=['POST'])
def delete(id):
    post = get_post(id)
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if current_user.username != 'admin':
        abort(403)

    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted from the posts!'.format(
        post['title']))
    return redirect(url_for('main.posts'))

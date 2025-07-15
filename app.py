from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import UPLOAD_FOLDER, SECRET_KEY
from utils import allowed_file, save_image
from db import get_db_connection
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT posts.id, posts.title, posts.content, posts.image, posts.user_id, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.id DESC
    """)
    posts = cur.fetchall()
    conn.close()
    return render_template('home.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
            flash('Registration successful.')
            return redirect(url_for('login'))
        except:
            flash('Username already exists.')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user'] = user['username']
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.')
    return redirect(url_for('home'))

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        flash('Login required.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = request.files['image']

        image_name = None
        if image_file and allowed_file(image_file.filename):
            image_name = save_image(image_file)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO posts (title, content, image, user_id) VALUES (%s, %s, %s, %s)",
                    (title, content, image_name, session['user_id']))
        conn.commit()
        conn.close()
        flash('Post created.')
        return redirect(url_for('home'))

    return render_template('create_post.html')

@app.route('/post/<int:id>')
def view_post(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT posts.id, posts.title, posts.content, posts.image, posts.user_id, users.username
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = %s
    """, (id,))
    post = cur.fetchone()
    conn.close()
    return render_template('view_post.html', post=post)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if 'user_id' not in session:
        flash('Login required.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cur.fetchone()

    if not post or post['user_id'] != session['user_id']:
        flash('Unauthorized.')
        conn.close()
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = request.files['image']

        image_name = post['image']
        if image_file and allowed_file(image_file.filename):
            image_name = save_image(image_file)

        cur.execute("UPDATE posts SET title = %s, content = %s, image = %s WHERE id = %s",
                    (title, content, image_name, id))
        conn.commit()
        conn.close()
        flash('Post updated.')
        return redirect(url_for('home'))

    conn.close()
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_post(id):
    if 'user_id' not in session:
        flash('Login required.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM posts WHERE id = %s", (id,))
    post = cur.fetchone()

    if not post or post['user_id'] != session['user_id']:
        flash('Unauthorized.')
    else:
        cur.execute("DELETE FROM posts WHERE id = %s", (id,))
        conn.commit()
        flash('Post deleted.')

    conn.close()
    return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    if not os.path.exists('static/pics'):
        os.makedirs('static/pics')
    app.run(debug=True)

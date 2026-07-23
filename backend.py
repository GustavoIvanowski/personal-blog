from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

# App and Database setup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

auth = HTTPBasicAuth()
load_dotenv()

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Blog id={self.id} title='{self.title}'>"

# Authentication

users = {
    os.environ["ADMIN_USERNAME"]:
        generate_password_hash(os.environ["ADMIN_PASSWORD"])
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username], password):
        return username

# Routez

@app.route("/")
def home():
    posts = Blog.query.order_by(Blog.date_created).all()
    return render_template('guest/home.html', posts=posts)

@app.route("/admin")
@auth.login_required
def dashboard():
    posts = Blog.query.order_by(Blog.date_created).all()
    return render_template('admin/dashboard.html', posts=posts)

@app.route("/post/<int:id>")
def post(id):
    post = Blog.query.get_or_404(id)
    return render_template("/guest/post.html", post=post)

@app.route("/admin/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        postTitle = request.form['title']
        postContent = request.form['content']
        newPost = Blog(title=postTitle, content=postContent)

        try:
            db.session.add(newPost)
            db.session.commit()
            return redirect('/admin')
        except Exception as e:
            return str(e)
    else:
        return render_template('admin/add.html')

@app.route("/admin/edit/<int:id>", methods=['POST','GET'])
def update(id):
    post = Blog.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/admin')
        except Exception as e:
            return str(e)
    else:
        return render_template('admin/update.html', post=post)

@app.route("/admin/delete/<int:id>")
def delete(id):
    post = Blog.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/admin')
    except Exception as e:
        return str(e)


# test
if __name__ == "__main__":
    app.run(debug=True)
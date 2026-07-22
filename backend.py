from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Blog id={self.id} title='{self.title}'>"

@app.route("/")
def home():
    posts = Blog.query.order_by(Blog.date_created).all()
    return render_template('guest/home.html', posts=posts)

@app.route("/admin")
def dashboard():
    posts = Blog.query.order_by(Blog.date_created).all()
    return render_template('admin/dashboard.html', posts=posts)

@app.route("/admin/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        postTitle = request.form['title']
        postContent = request.form['content']
        newPost = Blog(title=postTitle, content=postContent)

        try:
            db.session.add(newPost)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return str(e)
    else:
        return render_template('admin/add.html')

@app.route("/admin/edit/<int:id>", methods=['POST','GET'])
def update(id):
    post = Blog.query.get_or_404(id)
    if request.method == 'POST':
        pass
    else:
        return render_template('admin/update.html', post=post)
    


# test
if __name__ == "__main__":
    app.run(debug=True)
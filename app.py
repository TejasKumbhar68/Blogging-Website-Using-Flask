from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
from datetime import datetime

app=Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY']='secret'
db = SQLAlchemy(app)
app.app_context().push()
login_manager=LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Blog(db.Model):
    blog_id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80), nullable=False)
    author=db.Column(db.String(50), nullable=False)
    content=db.Column(db.Text(), nullable=False)
    pub_date=db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return '<Blog {}>'.format(self.title)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def index():
    data=Blog.query.all()
    return render_template("index.html", data=data)

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        username=request.form.get('uname')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        user=User(username=username, email=email, fname=fname, lname=lname, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registed Successfully','success')
        return redirect('/login')

    return render_template("register.html")

@app.route("/login", methods=['GET','POST'])
def login():

    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter_by(username=username).first()

        if user and password==user.password:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid Credentials','warning')
            return redirect('/login')
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route("/blogpost", methods=['GET','POST'])
def blogpost():
    if request.method=='POST':
        title=request.form.get('title')
        author=request.form.get('author')
        content=request.form.get('content')
        blog=Blog(title=title, author=author, content=content)
        db.session.add(blog)
        db.session.commit()
        flash('Post added Successfully','success')
        return redirect('/')
    return render_template('blog.html')

@app.route("/blogdetail/<int:id>", methods=['GET','POST'])
def blogdetail(id):
    blog=Blog.query.get(id)
    return render_template('blogdetail.html',blog=blog)

@app.route("/delete/<int:id>", methods=['GET','POST'])
def delete(id):
    blog=Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash('Post has been deleted','success')
    return redirect('/')

@app.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    blog=Blog.query.get(id)
    if request.method=='POST':
        blog.title=request.form.get('title')
        blog.author=request.form.get('author')
        blog.content=request.form.get('content')
        db.session.commit()
        flash('Post has been updated','success')
        return redirect('/')
    return render_template('/edit.html', blog=blog)

if __name__=="__main__":
    app.run(debug=True)
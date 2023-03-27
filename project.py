from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wjievbaiwds;vjk.v,lkasdhflaksdnhlkfzhxdkv.zskljgvsbfjklvz.,mxc,.cbjklvarhfd;ncjz.f,zhv.cmz cx nn'


app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique =True, nullable=False)
    email = db.Column(db.String(120), unique =True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    
    


@app.route("/")
@app.route("/home", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        post_name = request.form['name']
        post_content = request.form['content']
        new_post = Post(title=post_name, content = post_content)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/home')
        except:
            return "Error"
    else:
        posts = Post.query.order_by(Post.date_posted)
        return render_template('home.html', posts=posts)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html')

@app.route("/signup")
def signup():
    form = RegistrationForm()
    return render_template('signup.html', form=form)

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
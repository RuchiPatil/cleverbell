from datetime import datetime
from forms import RegistrationForm, LoginForm
from flask import Flask, render_template, url_for, flash, redirect  #importing flask class and templates folders **ensure folder is called Templates with an s
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #creating app variable "__name__ is name of module"
app.config['SECRET_KEY'] = '41c3c5eef769fc02139d720817780103'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [

    {
        'author': 'Sentha',
        'title': 'Blog Post',
        'content': 'First Post',
        'date_posted': '5/28/2022'
    },
    {
        'author': 'Sentha',
        'title': 'Blog Post 2',
        'content': 'Second Post',
        'date_posted': '5/29/2022'
    }


]


@app.route("/") #rootpage of website or home page
@app.route("/home") #tworoutes handled by same function
def home():
    return render_template('home.html',posts=posts) #pulls html codes from folder using render templates/ will now be able to access post created a variable by creating an argument
# decorators are ways to add functionality

@app.route("/about") #rootpage of website about page
def about():
    return render_template('about.html',title='About') 

@app.route("/register", methods=['GET', 'POST']) #rootpage of website about page
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success') #validate that user acc is created
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST']) #rootpage of website about page
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'sendu319@hotmail.com' and form.password.data == 'Lithu1995':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login UnSuccessful. please check and try again', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__': #name is main
    app.run(debug=True) #only true if running the script directly


from datetime import datetime
from forms import RegistrationForm, LoginForm
from flask import Flask, render_template, url_for, flash, redirect, request, session  #importing flask class and templates folders **ensure folder is called Templates with an s
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from authlib.integrations.flask_client import OAuth

app = Flask(__name__) #creating app variable "__name__ is name of module"
app.config['SECRET_KEY'] = '41c3c5eef769fc02139d720817780103'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.db'
db = SQLAlchemy(app) #initialize the db

oauth = OAuth(app)

app.config['GOOGLE_CLIENT_ID'] = "12437568672-l57ij1ks79uh1laqs27ppf0ti1bjnpjl.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"

google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_uri = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs = {'scope': 'openid email profile'},
    #server_metadata_url=f'https://{set("AUTH_DOMAIN")}/.well-known/openid-configuration'
)


#create a model to see if db works
#class Friends(db.Model):
   # id = db.Column(db.Integer, primary_key=True)
   # name =  db.Column(db.String(200), nullable=False)
   # date_created = db.Column(db.DateTime, default=datetime.utcnow)

    #create a fuction to return a string when we add to db
   # def __repr__(self):
    #    return '<Name %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

posts = [

    {
        'title': 'Event History',
        'content': 'First Event',
        'date_posted': '5/28/2022'
    }
    
]


@app.route("/") #rootpage of website or home page
@app.route("/home") #tworoutes handled by same function
def home():
    email = dict(session).get('email',None)
    return f'Hello, {email}!'
    return render_template('home.html',posts=posts) #pulls html codes from folder using render templates/ will now be able to access post created a variable by creating an argument
# decorators are ways to add functionality

@app.route("/about") #rootpage of website about page
def about():
    return render_template('about.html',title='About') 

@app.route("/friends", methods=['GET', 'POST']) #rootpage of website about page
def friends():

    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)

        #push to db
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "there was an error adding your Friends  "
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html',title='friends')

@app.route("/register", methods=['GET', 'POST']) #rootpage of website about page
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New User has been created</h1>'
     #   return '<h1>' + form.username.data + '' + form.email.data + '' + form.password.data + '</h1>'

    return render_template('register.html', form=form)
    
@app.route("/login", methods=['GET', 'POST']) #rootpage of website about page
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user: #check if user exist
            if user.password == form.password.data:
                return redirect(url_for('home')) #if ogin successful return to home page

        return '<h1>Invalid username or password</h1>'

       # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html',form=form)

@app.route('/google_login')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/google_authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    return "you are signed in"

if __name__ == '__main__': #name is main
    app.run(debug=True) #only true if running the script directly


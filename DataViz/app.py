from collections import UserDict, UserList
import MySQLdb
from flask import Flask, flash, redirect,render_template, request, session, url_for
from flask_cors import CORS
from flask_login import LoginManager, UserMixin,login_user
import mysqlx
from db import db
from visitorlog import visitor_blueprint
from dashboard import dashboard_blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required,current_user

app=Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'


#database cofiguration 
username="root"
password=""
userpass='mysql+pymysql://'+username+':'+password+'@'
server='127.0.0.1'
dbname='/wallmart_visitors'

app.config['SQLALCHEMY_DATABASE_URI']=userpass+server+dbname
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True
db.init_app(app)
#register blueprint
app.register_blueprint(visitor_blueprint)
app.register_blueprint(dashboard_blueprint)



# @app.route('/')
# def server_status():

#    return "Server is up and running"
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

class User(UserMixin,db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,primary_key = True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phonenumber = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return self.username

@app.route('/')
def index1():
    return render_template('register.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phonenumber = request.form['phonenumber']
        address = request.form['address']

        new_user = User(username=username, password=password, phonenumber=phonenumber, address=address)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username,password=password).first()
        # print(user,password)
        if user :
            flash('Login success','primary')
            session['logged_in']=True
            session ['username']=username
          #  print(username,password)
            login_user(user)
            print(current_user.username)
            return redirect('/index')
        if current_user.is_authenticated:
            return redirect('/index')  
        else:
            flash("Invalid credential",'danger')
            # print(user.password, password)
            return render_template("login.html")
    # a = User.query.all()
    # print(a)
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard1')
def dashboard1():
    return render_template('dashboard1.html')
   
   #return "Server is up and running"
   

#     return render_template(index.html)



if __name__ == '__main__':
    app.run(debug=True)
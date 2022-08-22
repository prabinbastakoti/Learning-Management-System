
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'afaf8a7f6a76f9af7afbjkaf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # To Create database named site.db in current directory.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from lmsproject import routes
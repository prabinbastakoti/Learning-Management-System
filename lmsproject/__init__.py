
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'afaf8a7f6a76f9af7afbjkaf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # To Create database named site.db in current directory.
db = SQLAlchemy(app)

from lmsproject import routes
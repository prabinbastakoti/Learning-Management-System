
from flask import render_template, url_for, flash, redirect, request
from lmsproject import app, db, bcrypt
from lmsproject.forms import LoginForm, RegistrationForm
from lmsproject.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Login Successful.",'success')
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            flash("Login Unsuccessful. Please check email and password",'danger')
    form.email.data=''    
    return render_template('login.html',form = form)


@app.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname = form.firstname.data, lastname = form.lastname.data, email = form.email.data,\
                     phonenumber=form.phonenumber.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('signup.html',form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))  



@app.route('/account')
@login_required
def account():
    return render_template('account.html')

from flask import render_template, url_for, flash, redirect, request
from lmsproject import app, db, bcrypt
from lmsproject.forms import LoginForm, RegistrationForm
from lmsproject.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',title='Home')



@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("faculty"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Login Successful. Welcome to Shikshyalaya {current_user.firstname} {current_user.lastname}.",'success')
            return redirect(next_page) if next_page else redirect(url_for('faculty')) 
        else:
            flash("Credentials do not match our records. Please Try Again.",'danger')
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
                    birthday=form.birthday.data, phonenumber=form.phonenumber.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('signup.html',form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out Successfully!','success')
    return redirect(url_for('home'))  





@app.route('/elearningunit1')
@login_required
def elearningunit1():
    return render_template('elearningunit1.html')

@app.route('/elearningunit2')
@login_required
def elearningunit2():
    return render_template('elearningunit2.html')

@app.route('/elearning')
@login_required
def elearning():
    return render_template('elearning.html')

@app.route('/faculty')
@login_required
def faculty():
    return render_template('faculty.html')

@app.route('/semester')
@login_required
def semester():
    return render_template('semester.html')

@app.route('/subject')
@login_required
def subject():
    return render_template('subject.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

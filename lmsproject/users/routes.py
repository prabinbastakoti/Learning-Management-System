import os
from flask import (render_template, url_for,flash, redirect, request, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from lmsproject import db, bcrypt
from lmsproject.models import User, Post
from lmsproject.users.forms import (RegistrationForm, LoginForm, EditProfileForm, RequestResetForm, ResetPasswordForm)
from lmsproject.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)

@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.faculty"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Login Successful. Welcome to Shikshyalaya {current_user.firstname} {current_user.lastname}.",'success')
            return redirect(next_page) if next_page else redirect(url_for('main.faculty')) 
        else:
            flash("Credentials do not match our records. Please Try Again.",'danger')
    form.email.data=''    
    return render_template('users/login.html',form = form,title='Login')



@users.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.gender.data =='Male':
            image_file = (os.path.basename("/static/images/profile_pics/"+ "male.svg"))
        elif form.gender.data =="Female":
            image_file = (os.path.basename("/static/images/profile_pics/"+ "female.svg"))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstname = form.firstname.data, lastname = form.lastname.data, email = form.email.data,\
                    birthdate=form.birthdate.data,gender=form.gender.data, phonenumber=form.phonenumber.data, password = hashed_password, \
                        address=form.address.data,university=form.university.data,college=form.college.data,regnum=form.regnum.data,
                        image_file=image_file)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('users.login'))
    return render_template('users/signup.html',form = form,title='SignUp')



@users.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out Successfully!','success')
    return redirect(url_for('main.home'))


@users.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    image_file = url_for('static',filename='images/profile_pics/'+ current_user.image_file )
    return render_template('users/profile.html',title='Profile',
                             image_file = image_file)






@users.route('/editprofile',methods=['GET','POST'])
@login_required
def editprofile():
    form = EditProfileForm()
    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.phonenumber = form.phonenumber.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('users.profile'))

    elif request.method == 'GET':
        form.phonenumber.data = current_user.phonenumber
        form.email.data = current_user.email

    image_file = url_for('static',filename='images/profile_pics/'+ current_user.image_file )
    return render_template('users/editprofile.html',title='Edit Profile',
                             image_file = image_file ,form = form)


@users.route("/user/<string:email>",methods=['GET','POST'])
@login_required
def user_posts(email):
    page = request.args.get('page',1, type=int)
    user = User.query.filter_by(email=email).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=5)
    return render_template('users/user_posts.html',posts = posts, user=user)


@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('users.login'))
    form.email.data =''
    return render_template('users/reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in','success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html',title='Reset Password',form=form)
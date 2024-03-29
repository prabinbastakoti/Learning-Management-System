import os
from flask import (render_template, url_for,flash, redirect, request, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from lmsproject import db, bcrypt
from lmsproject.models import User, Post
from lmsproject.users.forms import (RegistrationForm, LoginForm, EditProfileForm1, EditProfileForm2,
                                    RequestResetForm, ResetPasswordForm)
from lmsproject.users.utils import save_picture, send_reset_email
from werkzeug.datastructures import CombinedMultiDict


users = Blueprint('users', __name__)


@users.route('/editprofile', methods=['GET','POST'])
@login_required
def editprofile():  

    form = EditProfileForm1(CombinedMultiDict((request.files, request.form)))

    if request.method =='POST' and form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phonenumber = form.phonenumber.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.birthdate = form.birthdate.data
        current_user.gender = form.gender.data
        current_user.address = form.address.data

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        elif form.picture.data is None:
            if current_user.image_file in ['male.svg','female.svg']:
                if form.gender.data =='Male':
                    current_user.image_file = (os.path.basename("/static/images/profile_pics/"+ "male.svg"))
                elif form.gender.data =="Female":
                    current_user.image_file = (os.path.basename("/static/images/profile_pics/"+ "female.svg"))

        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for("users.profile"))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.gender.data = current_user.gender
        form.email.data = current_user.email
        form.phonenumber.data = current_user.phonenumber
        form.address.data = current_user.address

    image_file = url_for('static',filename='images/profile_pics/'+ current_user.image_file )
    return render_template('users/editprofile.html',title='Edit profile',
                            image_file=image_file, form=form)


@users.route("/editprofile/deletephoto", methods=['POST'])
@login_required
def delete_photo():
    
    if current_user.gender == 'Male':
        current_user.image_file = (os.path.basename("/static/images/profile_pics/"+ "male.svg"))

    elif current_user.gender == "Female":
        current_user.image_file = (os.path.basename("/static/images/profile_pics/"+ "female.svg"))

    db.session.commit()
    flash('Your Photo has been deleted!','success')
    return redirect(url_for('users.profile'))



@users.route('/editprofile2',methods=['GET','POST'])
@login_required
def editprofile2():
    form = EditProfileForm2(CombinedMultiDict((request.files, request.form)))

    if request.method =="POST" and form.validate_on_submit():
        current_user.university = form.university.data
        current_user.college = form.college.data
        current_user.faculty = form.faculty.data
        current_user.semester = form.semester.data
        current_user.regnum = form.regnum.data
        current_user.skill1 = form.skill1.data
        current_user.skill2 = form.skill2.data
        current_user.skill3 = form.skill3.data
        current_user.skill4 = form.skill4.data
        current_user.skill5 = form.skill5.data
        current_user.skill6 = form.skill6.data
        current_user.skill7 = form.skill7.data
        current_user.skill8 = form.skill8.data
        current_user.skill9 = form.skill9.data
        current_user.skill10 = form.skill10.data

        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for("users.profile"))

    elif request.method == "GET":
        form.university.data = current_user.university
        form.college.data = current_user.college
        form.faculty.data = current_user.faculty
        form.semester.data = current_user.semester
        form.regnum.data = current_user.regnum

        if current_user.skill1 == "1":
            form.skill1.data = current_user.skill1
        else:
            form.skill1.data =  None

        if current_user.skill2== "1":
            form.skill2.data = current_user.skill2
        else:
            form.skill2.data =  None

        if current_user.skill3== "1":
            form.skill3.data = current_user.skill3
        else:
            form.skill3.data =  None

        if current_user.skill4== "1":
            form.skill4.data = current_user.skill4
        else:
            form.skill4.data =  None

        if current_user.skill5== "1":
            form.skill5.data = current_user.skill5
        else:
            form.skill5.data =  None

        if current_user.skill6== "1":
            form.skill6.data = current_user.skill6
        else:
            form.skill6.data =  None

        if current_user.skill7== "1":
            form.skill7.data = current_user.skill7
        else:
            form.skill7.data =  None

        if current_user.skill8== "1":
            form.skill8.data = current_user.skill8
        else:
            form.skill8.data =  None

        if current_user.skill9== "1":
            form.skill9.data = current_user.skill9
        else:
            form.skill9.data =  None

        if current_user.skill10== "1":
            form.skill10.data = current_user.skill10
        else:
            form.skill10.data =  None
    
    return render_template('users/editprofile2.html',title='Edit profile',form=form)
                            


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
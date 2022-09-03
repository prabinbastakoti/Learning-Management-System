import secrets
from PIL import Image
import os
from flask import render_template, url_for, flash, redirect, request, abort
from lmsproject import app, db, bcrypt
from lmsproject.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from lmsproject.models import User , Post
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
    return render_template('login.html',form = form,title='Login')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname = form.firstname.data, lastname = form.lastname.data, email = form.email.data,\
                    birthdate=form.birthdate.data,gender=form.gender.data, phonenumber=form.phonenumber.data, password = hashed_password, \
                        address=form.address.data,university=form.university.data,college=form.college.data,regnum=form.regnum.data,)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    return render_template('signup.html',form = form,title='SignUp')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out Successfully!','success')
    return redirect(url_for('home'))  





@app.route('/elearningunit1')
@login_required
def elearningunit1():
    return render_template('elearningunit1.html',title='E-learning Unit1')

@app.route('/elearningunit2')
@login_required
def elearningunit2():
    return render_template('elearningunit2.html',title='E-learning Unit2')

@app.route('/elearningunit4')
@login_required
def elearningunit4():
    return render_template('elearningunit4.html',title='E-learning Unit4')

@app.route('/elearning')
@login_required
def elearning():
    return render_template('elearning.html',title='E-learning')

@app.route('/faculty')
@login_required
def faculty():
    return render_template('faculty.html',title='Faculty')

@app.route('/semester')
@login_required
def semester():
    return render_template('semester.html',title='Semester')

@app.route('/subject')
@login_required
def subject():
    return render_template('subject.html',title='Subject')

@app.route('/forum')
@login_required
def forum():
    return render_template('forum.html',title='Forum')

@app.route('/profile')
@login_required
def profile():
    image_file = url_for('static',filename='images/profile_pics/'+ current_user.image_file )
    return render_template('profile.html',title='Profile',
                             image_file = image_file)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/images/profile_pics', picture_fn)
    
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)

    return picture_fn

@app.route('/editprofile', methods=['GET','POST'])
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
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.phonenumber.data = current_user.phonenumber
        form.email.data = current_user.email

    image_file = url_for('static',filename='images/profile_pics/'+ current_user.image_file )
    return render_template('editprofile.html',title='Edit Profile',
                             image_file = image_file ,form = form)


@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('community'))

    return render_template('create_post.html',title='New Post', form = form, legend = 'New Post') 


@app.route('/community')
@login_required
def community():
    posts = Post.query.all()
    return render_template('community.html',title='Community',posts = posts)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)



@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',
                            form = form, legend = 'Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('community'))
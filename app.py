 
from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'afaf8a7f6a76f9af7afbjkaf'

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been Logged In Successfully!','success')
            return redirect(url_for('home'))
        else:
            flash("The email you entered isn't connected to an account.",'danger')
    form.email.data=''
    return render_template('login.html', form = form)


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Creation Success For {form.firstname.data} {form.lastname.data}.Please login to proceed.','success')
        return redirect(url_for('login'))
    form.firstname.data=''
    form.lastname.data=''
    form.email.data=''
    form.phonenumber.data=''
    return render_template('signup.html',form = form)



if __name__ == '__main__':
    app.run(debug=True)
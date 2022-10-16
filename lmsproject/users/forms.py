from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, DateField, RadioField,
                    PasswordField, SubmitField, BooleanField)
from wtforms.validators import (DataRequired, Length, Email, Optional,
                                EqualTo, ValidationError)
from lmsproject.models import User




class RegistrationForm(FlaskForm):

    username = StringField('Username',
                            validators=[DataRequired()])

    firstname = StringField('First Name',
                            validators=[DataRequired(),Length(min=2,max=20)])
    lastname = StringField('Last Name',
                            validators=[DataRequired(),Length(min=2,max=20)])

    birthdate =DateField('Date Of Birth',format='%Y-%m-%d',validators=[DataRequired()])

    gender = RadioField('Gender',validators=[DataRequired()], choices = [('Male','Male'),('Female','Female')],default='Male')

    email = StringField('Email Address',
                        validators= [DataRequired(), Email()])

    phonenumber= StringField('Phone Number', validators=[DataRequired(),Length(min=10,max=20)])

    address= StringField('Address', validators=[DataRequired()])

    university= StringField('University', validators=[DataRequired()])

    college= StringField('College', validators=[Optional()])

    regnum= StringField('Regd. No.', validators=[Optional()])

    password = PasswordField('Password',validators=[DataRequired(),Length(8)])

    confirmpassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email is already used.')

    def validate_phonenumber(self, phonenumber):
        user = User.query.filter_by(phonenumber = phonenumber.data).first()
        if user:
            raise ValidationError('Phonenumber is already used.')

    def validate_regnum(self, regnum):
        user = User.query.filter_by(regnum=regnum.data).first()
        if user:
            raise ValidationError('This Registration Number is associated with another Student. Please enter your valid Registration Number.')



class LoginForm(FlaskForm):
    email = StringField('Email Address',
                        validators= [ DataRequired(), Email()])

    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')



class EditProfileForm1(FlaskForm):

    username = StringField('Username',
                            validators=[DataRequired()])

    firstname = StringField('First Name',
                            validators=[DataRequired(),Length(min=2,max=20)])
    lastname = StringField('Last Name',
                            validators=[DataRequired(),Length(min=2,max=20)])

    birthdate =DateField('Date Of Birth',format='%Y-%m-%d',validators=[DataRequired()])

    gender = RadioField('Gender',validators=[DataRequired()], choices = [('Male','Male'),('Female','Female')],default='Male')

    email = StringField('Email Address',
                        validators= [DataRequired(), Email()])

    phonenumber= StringField('Phone Number', validators=[DataRequired(),Length(min=10,max=20)])

    address= StringField('Address', validators=[DataRequired()])

    picture = FileField('Update New Image', validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('An account with that username already exists. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('An account with that email already exists. Please choose a different one.')
                
    def validate_phonenumber(self, phonenumber):
        if phonenumber.data != current_user.phonenumber:
            user = User.query.filter_by(phonenumber=phonenumber.data).first()
            if user:
                raise ValidationError('An account with that phonenumber already exists. Please choose a different one.')


class EditProfileForm2(FlaskForm):

    university= StringField('University', validators=[DataRequired()])

    college= StringField('College', validators=[Optional()])

    faculty= StringField('Faculty', validators=[Optional()])

    semester= StringField('Semester', validators=[Optional()])

    college= StringField('College', validators=[Optional()])

    regnum= StringField('Regd. No.', validators=[Optional()])

    skill1= BooleanField('CyberSecurity',validators=[Optional()],default='0')

    skill2= BooleanField('Cloud Computing',validators=[Optional()],default='0')

    skill3= BooleanField('Data analytics and data science',validators=[Optional()],default='0')

    skill4= BooleanField('Networking and wireless',validators=[Optional()],default='0')

    skill5= BooleanField('Software Development',validators=[Optional()],default='0')

    skill6= BooleanField('AI & Machine learning',validators=[Optional()],default='0')

    skill7= BooleanField('Project management',validators=[Optional()],default='0')

    skill8= BooleanField('Programming',validators=[Optional()],default='0')

    skill9= BooleanField('IT service management',validators=[Optional()],default='0')

    skill10= BooleanField('Virtualization',validators=[Optional()],default='0')

    submit = SubmitField('Save Changes')


    def validate_regnum(self, regnum):
        if regnum.data != current_user.regnum:
            user = User.query.filter_by(regnum=regnum.data).first()
            if user:
                raise ValidationError('This Registration Number is associated with another Student. Please enter your valid Registration Number.')



class RequestResetForm(FlaskForm):

    email = StringField('Enter Your Email Address',
                        validators= [DataRequired(), Email()])

    submit = SubmitField('Forget Password')
                    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')



class ResetPasswordForm(FlaskForm):

    password = PasswordField('New Password',validators=[DataRequired(),Length(8)])

    confirmpassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Reset Password')
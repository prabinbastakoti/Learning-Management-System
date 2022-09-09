from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, DateField, RadioField,
                    PasswordField, SubmitField, BooleanField)
from wtforms.validators import (DataRequired, Length, Email, Optional,
                                EqualTo, ValidationError)
from lmsproject.models import User




class RegistrationForm(FlaskForm):
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

    university= StringField('University Name', validators=[DataRequired()])

    college= StringField('College Name', validators=[Optional()])

    regnum= StringField('Regd. No.', validators=[Optional()])

    password = PasswordField('Password',validators=[DataRequired(),Length(8)])

    confirmpassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email is already used.')

    def validate_phonenumber(self, phonenumber):
        user = User.query.filter_by(phonenumber = phonenumber.data).first()
        if user:
            raise ValidationError('Phonenumber is already used.')



class LoginForm(FlaskForm):
    email = StringField('Email Address',
                        validators= [ DataRequired(), Email()])

    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')



class EditProfileForm(FlaskForm):
    phonenumber= StringField('Phone Number', validators=[DataRequired(),Length(min=10,max=20)])

    email = StringField('Email Address',
                        validators= [DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')

    

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('This Email Address is already used. Please choose a different one.')
                
    def validate_phonenumber(self, phonenumber):
        if phonenumber.data != current_user.phonenumber:
            user = User.query.filter_by(phonenumber = phonenumber.data).first()
            if user:
                raise ValidationError('This Phonenumber is already used. Please choose a different one.')



class RequestResetForm(FlaskForm):

    email = StringField('Email Address',
                        validators= [DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')
                    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')



class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password',validators=[DataRequired(),Length(8)])

    confirmpassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Reset Password')
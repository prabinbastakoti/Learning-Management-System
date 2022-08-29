
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from lmsproject.models import User

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(),Length(min=2,max=20)])
    lastname = StringField('Last Name',
                            validators=[DataRequired(),Length(min=2,max=20)])

    birthdate =DateField('Birthdate',format='%Y-%m-%d',validators=[DataRequired()])

    gender = RadioField('Gender',validators=[DataRequired()], choices = [('Male','Male'),('Female','Female')],default='Male')

    email = StringField('Email Address',
                        validators= [DataRequired(), Email()])

    phonenumber= StringField('Phone Number', validators=[DataRequired(), Length(10)])

    address= StringField('Address', validators=[DataRequired()])

    university= StringField('University Name', validators=[DataRequired()])

    college= StringField('College Name', validators=[DataRequired()])

    regnum= StringField('Regd. No.(Optional)', validators=[Optional()])

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

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from lmsproject.models import User

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(),Length(min=2,max=20)])
    lastname = StringField('Last Name',
                            validators=[DataRequired(),Length(min=2,max=20)])

    email = StringField('Email Address',
                        validators= [DataRequired(), Email()])

    phonenumber= StringField('Phone Number', validators=[DataRequired(), Length(10)])

    password = PasswordField('Password',validators=[DataRequired()])

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
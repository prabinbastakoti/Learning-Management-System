
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, DateTimeField 
from wtforms.validators import DataRequired, Length, Email, EqualTo


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



class LoginForm(FlaskForm):
    email = StringField('Email Address',
                        validators= [ DataRequired(), Email()])

    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
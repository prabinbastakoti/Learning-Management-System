from lmsproject import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from datetime import datetime
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20),unique=True,nullable=False)
    firstname = db.Column(db.String(20), nullable= False)
    lastname = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False)
    phonenumber = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable= False)
    birthdate = db.Column(db.String(20),nullable=False)
    gender = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(30),nullable=False)
    university = db.Column(db.String(50),nullable=False)
    college = db.Column(db.String(50),nullable=True)
    regnum = db.Column(db.String(20),unique=True,nullable=True)
    faculty = db.Column(db.String(100),nullable=True)
    semester = db.Column(db.String(100),nullable=True)
    skill1 = db.Column(db.String(1000),nullable=True)
    skill2 = db.Column(db.String(1000),nullable=True)
    skill3 = db.Column(db.String(1000),nullable=True)
    skill4 = db.Column(db.String(1000),nullable=True)
    skill5 = db.Column(db.String(1000),nullable=True)
    skill6 = db.Column(db.String(1000),nullable=True)
    skill7 = db.Column(db.String(1000),nullable=True)
    skill8 = db.Column(db.String(1000),nullable=True)
    skill9 = db.Column(db.String(1000),nullable=True)
    skill10 = db.Column(db.String(1000),nullable=True)


    posts = db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.phonenumber}' ,'{self.image_file}')"

    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
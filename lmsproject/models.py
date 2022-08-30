from lmsproject import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable= False)
    lastname = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default= 'default.jpg')
    phonenumber = db.Column(db.Integer,unique=True,nullable=False)
    password = db.Column(db.String(60),nullable= False)
    birthdate = db.Column(db.String(20),nullable=False)
    gender = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(30),nullable=False)
    university = db.Column(db.String(50),nullable=False)
    college = db.Column(db.String(50),nullable=True)
    regnum = db.Column(db.String(20),nullable=True)

    
    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}','{self.email}','{self.image_file}')"

    
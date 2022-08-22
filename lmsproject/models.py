from lmsproject import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable= False)
    lastname = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default= 'default.jpg')
    phonenumber = db.Column(db.Integer,nullable=False)
    password = db.Column(db.String(60),nullable= False)
    
    def __repr__(self):
        return f"User('{self.firstname}','{self.lastname}','{self.email}','{self.image_file}')"

    
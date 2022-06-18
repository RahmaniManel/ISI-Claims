from datetime import datetime
from appvf import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


#class student

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    nots = db.relationship('Note', backref='student', lazy=True)


    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

#classe Mater

class Mater(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    coff = db.Column(db.String(100))
    namespecialty = db.Column(db.String(100))
    namefeild = db.Column(db.String(100))
    nots = db.relationship('Note', backref='mater', lazy=True)

    
    
    def __init__(self, name, coff, namespecialty, namefeild):
        self.name = name
        self.coff = coff
        self.namespecialty = namespecialty
        self.namefeild = namefeild
      
#calss specialty
class Specialty(db.Model):
    __tablename__ = 'specialty'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))  
   
    def __init__(self, name,):
        self.name = name
       

class Feild(db.Model):
    __tablename__ = 'feild'
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    specialtyid = db.Column(db.String(30)) 
    def __init__(self, name,specialtyid):
        self.name = name
        self.specialtyid = specialtyid
       
  
class Group(db.Model):
    __tablename__ = 'group'
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    feildid = db.Column(db.Integer)
    def __init__(self, name,feildid):
        self.name = name
        self.feildid = feildid
  
class Note(db.Model):
    __tablename__ = 'note'
  
    id = db.Column(db.Integer, primary_key=True)
    note_ds = db.Column(db.Integer)
    note_examen = db.Column(db.Integer)
    note_TP = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    mater_id = db.Column(db.Integer, db.ForeignKey('mater.id'))

    def __init__(self, note_ds, note_examen, note_TP, student_id, mater_id):
        self.note_ds = note_ds
        self.note_examen = note_examen
        self.note_TP = note_TP
        self.mater_id = mater_id
        self.student_id = student_id

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    adminname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(300), nullable=False)
    def __repr__(self):
        return f"User('{self.adminname}', '{self.email}', '{self.image_file}')"
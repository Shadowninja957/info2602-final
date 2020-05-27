from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True ,nullable=False)
    email = db.Column(db.String(100), unique=True ,nullable=False)
    password = db.Column(db.String(50), unique=True ,nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    reacts = db.relationship('UserReact', backref='reactions', lazy=True, cascade="all, delete-orphan")

    def toDict(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password

        }
    ''' Reference from Lab 11'''
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')    
 
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    '''      End Reference   '''

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), unique=True ,nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reacts = db.relationship('UserReact', backref='postReact', lazy=True, cascade="all, delete-orphan")

    def getTotalLikes(self):
        likes = 0
        for reaction in self.reacts:
            if reaction.react == "like":
                likes += 1
        return likes

    def getTotalDislikes(self):
        dislikes = 0
        for reaction in self.reacts:
            if reaction.react == "dislike":
                dislikes += 1
        return dislikes
    
    def toDict(self):
        return{
            'post': self.text,
            'username': self.author.username,
            'likes': self.getTotalLikes(),
            'dislikes': self.getTotalDislikes()
        }       


class UserReact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    react = db.Column(db.String(10))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    postid = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
'''    
class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId =  db.Column(db.Integer, nullable=False)
    stream = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def toDict(self):
        return{
            'id': self.id,
            'studentId': self.studentId,
            'stream': self.stream,
            'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")
        }
'''
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True ,nullable=False)
    email = db.Column(db.String(80), unique=True ,nullable=False)
    password = db.Column(db.String(50), unique=True ,nullable=False)

    def toDict(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password

        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), unique=True ,nullable=False)

    def toDict(self):
        pass
       
class UserReact(db.Model):
    pass
    
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

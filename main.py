import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User, UserReact, Post #add application models

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
#   app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
  CORS(app)
  login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here (if using flask JWT)'''
# def authenticate(uname, password):
#   pass

# #Payload is a dictionary which is passed to the function by Flask JWT
# def identity(payload):
#   pass

# jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''
'''
@app.route('/')
def index():
    return render_template('app.html')

@app.route('/clientapp')
def client_app():
  return app.send_static_file('app.html')
'''

@app.route('/app', methods=['GET'])
@login_required
def application():
    posts = Post.query.all()
    return render_template('app.html', posts=posts)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('successful login.') 
            login_user(user)
            return redirect(url_for('application'))
        else:
            flash('Invalid username or password')
        return render_template('index.html')    
    
    return render_template('index.html')

''' Reference from Lab 11 url: "https://nmendez.app/info2602/lab11/#0"
        Took the basic template in repl.it and modified it     '''

@app.route('/createPost', methods=['POST'])
@login_required
def create_post():
  text = request.form['text']
  post = Post(text=text, userid=current_user.id)
  db.session.add(post)
  db.session.commit()
  flash('Created')
  return redirect(url_for('application'))

@app.route('/deletePost/<id>', methods=["GET"])
@login_required
def delete_post(id):
  post = Post.query.filter_by(userid=current_user.id, id=id).first()
  if post == None:
    flash ('Invalid id or unauthorized')
  db.session.delete(post)
  db.session.commit()
  flash ('Deleted!')
  return redirect(url_for('application'))

@app.route('/updatePost/<id>', methods=['POST'])
@login_required
def update_post(id):
    reaction = request.args.get('selection')
    post = Post.query.filter_by(id=id).first()
    if post == None:
        flash('Invalid id or unauthorized')
    react = UserReact.query.filter_by(react=reaction, userid=current_user.id, postid=post.id).first()
    if react == None: 
        react = UserReact(react=reaction, userid=current_user.id, postid=post.id)
        db.session.add(react)
        db.session.commit()
    else:
        react.react = reaction
    return redirect(url_for('application'))

'''      End Reference   '''

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)

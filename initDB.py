from main import app
from models import db, User, Post, UserReact

db.create_all(app=app)

user_1 = User(username="bob", email="bob@mail.com")
user_1.set_password('bobpass')

user_2 = User(username="alice", email="alice@mail.com")
user_2.set_password('alicepass')

db.session.add(user_1)
db.session.add(user_2)
db.session.commit()

print('database initialized!')
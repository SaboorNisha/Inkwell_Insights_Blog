import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask


db = SQLAlchemy()
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret key'  # Set a secret key for flashing messages

# Initialize the app with SQLAlchemy
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(500), nullable=False)
    Author = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(500), nullable=False)
    Slug = db.Column(db.String(200), nullable=False)
    blog_post = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Post {self.Title}>'
        
class User(UserMixin,db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(500), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(500), nullable=True)


    def set_password(self, password):
        self.Password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=10)

    def check_password(self, password):
        return check_password_hash(self.Password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
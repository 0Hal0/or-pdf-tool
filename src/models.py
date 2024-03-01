from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from werkzeug.security import generate_password_hash
from dotenv import dotenv_values

secrets = dotenv_values(".env")

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))
    userType = db.Column(db.String(100))

class UserTypes:
    owner = "Owner"
    admin = "Admin"
    user = "User"

class services(db.Model):
    id = db.Column(db.String(100), primary_key = True)
    


def generate_default_user():
    if not User.query.filter_by(username = secrets["DB_ADMIN_USER"]).all():
        print("Adding admin user")
        db.session.add(User(username = secrets["DB_ADMIN_USER"], password=generate_password_hash(secrets["DB_ADMIN_PASS"]), userType = UserTypes.owner))
        db.session.commit()
        print("Added admin user")      

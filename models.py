from flask_login import UserMixin
from database import db
from sqlalchemy.orm import relationship


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(50), nullable=False)
    toppings = db.Column(db.String(500), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=100)  # Add this line

    def __init__(self, name, price, size, toppings, stock=100):
        self.name = name
        self.price = price
        self.size = size
        self.toppings = toppings
        self.stock = stock



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    contacts = db.relationship('Contact', backref='user', lazy=True)
    is_employee = db.Column(db.Boolean, nullable=False, default=False)  # Add this line
    
    def __repr__(self):
        return '<User %r>' % self.username

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100))
    message = db.Column(db.String(100))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    pizza_id = db.Column(db.Integer, nullable=False)
    pizza_size = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Add this line

    def __repr__(self):
        return f"Order('{self.name}', '{self.email}', '{self.pizza_id}', '{self.pizza_size}')"


class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, nullable=False)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)



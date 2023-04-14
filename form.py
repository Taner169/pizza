from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, TextAreaField, BooleanField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, number_range, NumberRange, Optional
from models import *

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=50)])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=50)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=500)])



class OrderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pizza_type = SelectField('Pizza Type', coerce=int)
    pizza_size = SelectField('Pizza Size', choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    submit = SubmitField('Place Order')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.pizza_type.choices = [
            (pizza.id, f"{pizza.name} - ${pizza.price}")
            for pizza in Pizza.query.all()
        ]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user:
            raise ValidationError('Invalid username.')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            user = User.query.filter_by(email=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Invalid password.')


class AddPizzaForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    toppings = StringField('Toppings', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), number_range(min=0)])
    size = SelectField('Size', choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')])
    submit = SubmitField('Add Pizza')


class UpdateInventoryForm(FlaskForm):
    pizza_id = SelectField('Pizza', validators=[DataRequired()])
    name = StringField('Pizza Name', validators=[DataRequired()])
    toppings = StringField('Toppings')
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Update Inventory')


class RemovePizzaForm(FlaskForm):
    pizza_id = SelectField('Pizza ID', choices=[], coerce=int)
    submit = SubmitField('Remove Pizza')


class UpdatePizzaDetailsForm(FlaskForm):
    pizza_id = SelectField('Pizza', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[Optional()])
    toppings = StringField('Toppings', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Update Inventory')
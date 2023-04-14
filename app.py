from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import *
from flask_migrate import Migrate
from employee_views import employee_blueprint
from database import db
from form import *
from werkzeug.urls import url_parse



app = Flask(__name__, template_folder='templates')
app.register_blueprint(employee_blueprint, url_prefix='/employee')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurang.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'qweqwe qweqwe'

migrate = Migrate(app, db)
db.init_app(app)


# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Load the user from the database
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


@app.route('/')
def home():
    user = session.get('user', None)  # Get the logged-in user's username from the session, or None if not logged in
    return render_template('home.html', user=user)


@app.route('/menu')
def menu():
    all_pizzas = Pizza.query.all()
    return render_template('menu.html', pizzas=all_pizzas)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
        
        if user:
            if user.password == password: # You might want to use a hashing function here for better security
                login_user(user)
                return redirect('/')
            else:
                flash('Username and/or password is incorrect', 'error')
        else:
            flash('Username and/or password field is missing', 'error')
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        # Check if username and email already exist in database
        user = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        if user:
            error = "Username already exists. Please choose another one."
            return render_template('register.html', error=error)
        if email_exists:
            error = "Email already exists. Please use another email."
            return render_template('register.html', error=error)

        # Check if password and confirm password match
        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template('register.html', error=error)

        # Insert user information into database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        
        # Redirect to login page
        return redirect(url_for('login'))
    
    # If request method is GET, render the register page
    return render_template('register.html')





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/about-us')
def about():
    return render_template('about-us.html')


@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        user = None
        if current_user.is_authenticated:
            user = current_user._get_current_object()

        contact = Contact(user=user, name=name, email=email, subject=subject, message=message)
        db.session.add(contact)
        db.session.commit()

        flash('Your message has been sent successfully. We will contact you as soon as possible.', 'success')
        return render_template('contact-us.html')

    return render_template('contact-us.html')


@app.route("/create-order", methods=['GET', 'POST'])
@login_required
def create_order():
    form = OrderForm()
    form.pizza_type.choices = [(pizza.id, pizza.name) for pizza in Pizza.query.filter(Pizza.stock > 0).all()]
    
    if form.validate_on_submit():
        try:
            name = form.name.data
            email = form.email.data
            pizza_id = form.pizza_type.data
            pizza_size = form.pizza_size.data
            pizza = Pizza.query.get(pizza_id)
            if not pizza:
                raise Exception("Invalid pizza selection.")
            
            # Calculate the price based on the selected pizza's price and size
            if pizza_size == 'Medium':
                price = pizza.price + 2.0
            elif pizza_size == 'Large':
                price = pizza.price + 4.0
            else:
                price = pizza.price
            
            new_order = Order(name=name, email=email, pizza_id=pizza_id, pizza_size=pizza_size, price=price)
            
            # Update the pizza stock
            ordered_pizza = Pizza.query.get(pizza_id)
            if ordered_pizza and ordered_pizza.stock > 0:
                ordered_pizza.stock -= 1
                db.session.add(new_order)
                db.session.commit()

                # Update inventory items stock
                toppings = ordered_pizza.toppings.split(', ')
                for topping in toppings:
                    inventory_item = InventoryItem.query.filter_by(name=topping).first()
                    if inventory_item:
                        inventory_item.stock -= 1
                db.session.commit()

                return redirect(url_for('order_success', order_id=new_order.id))
            else:
                flash("Not enough stock for the ordered pizza!", "danger")
        except Exception as e:
            flash(f"Error placing order: {e}", "danger")
    return render_template('create-order.html', form=form)



if __name__ == '__main__':
    # Create the database if it doesn't exist
   with app.app_context():
       db.create_all()

    

   app.run(host='0.0.0.0', port=8080, debug=True)

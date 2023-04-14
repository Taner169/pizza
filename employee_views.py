from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User,  Pizza, Order
from form import AddPizzaForm, UpdateInventoryForm, RemovePizzaForm, InventoryItem, UpdatePizzaDetailsForm
from flask_login import login_user, login_required, current_user
from flask_migrate import Migrate
from sqlalchemy import func


employee_blueprint = Blueprint('employee', __name__, template_folder='templates')

migrate = Migrate(employee_blueprint, db)


@employee_blueprint.route('/employee-dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    add_form = AddPizzaForm(prefix='add')
    update_pizza_details_form = UpdatePizzaDetailsForm()
    remove_form = RemovePizzaForm(prefix='remove')
    pizzas = Pizza.query.all()
    update_pizza_details_form.pizza_id.choices = [(pizza.id, pizza.name) for pizza in pizzas]
    remove_form.pizza_id.choices = [(pizza.id, pizza.name) for pizza in pizzas]

    if add_form.submit.data and add_form.validate_on_submit():
        # Handle adding pizza
        pizza = Pizza(name=add_form.name.data, price=add_form.price.data, size=add_form.size.data, toppings=add_form.toppings.data)
        db.session.add(pizza)
        db.session.commit()
        flash('Pizza added successfully!', 'success')
        return redirect(url_for('employee.dashboard'))

    if update_pizza_details_form.submit.data and update_pizza_details_form.validate_on_submit():
        # Handle updating pizza
        pizza = Pizza.query.get(update_pizza_details_form.pizza_id.data)
        pizza.name = update_pizza_details_form.name.data
        pizza.toppings = update_pizza_details_form.toppings.data
        pizza.stock = update_pizza_details_form.stock.data
        db.session.commit()
        flash('Pizza updated successfully!', 'success')
        return redirect(url_for('employee.dashboard'))

    if remove_form.submit.data and remove_form.validate_on_submit():
        # Handle removing pizza
        pizza = Pizza.query.get(remove_form.pizza_id.data)
        db.session.delete(pizza)
        db.session.commit()
        flash('Pizza removed successfully!', 'success')
        return redirect(url_for('employee.dashboard'))

    return render_template('employee-dashboard.html', add_form=add_form, update_pizza_details_form=update_pizza_details_form, remove_form=remove_form, pizzas=pizzas)





@employee_blueprint.route('/employee-login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('employee.dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        print("Username:", username)
        print("Password:", password)
        print("User:", user)

        if user and user.password == password and user.is_employee:
            login_user(user)
            return redirect(url_for('employee.dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('employee-login.html')



@employee_blueprint.route('/employee-register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        # Automatically generate the email
        email = f"{username}@pizza-restaurang.com"
        
        # Check if username and email already exist in database
        user = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        if user:
            error = "Username already exists. Please choose another one."
            return render_template('employee-register.html', error=error)
        if email_exists:
            error = "Email already exists. Please use another email."
            return render_template('employee-register.html', error=error)

        # Check if password and confirm password match
        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template('employee-register.html', error=error)

        # Insert user information into database
        new_user = User(username=username, email=email, password=password, is_employee=True)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        
        # Redirect to login page
        return redirect(url_for('employee.login'))
    
    # If request method is GET, render the register page
    return render_template('employee-register.html')




@employee_blueprint.route('/sales-data', methods=['GET'])
@login_required
def sales_data():
    # Retrieve all orders
    orders = Order.query.all()

    # Calculate the total number of orders
    total_orders = len(orders)

    # Calculate the total revenue
    total_revenue = sum(order.price for order in orders)

    return render_template('sales-data.html', total_orders=total_orders, total_revenue=total_revenue)


@employee_blueprint.route('/employee/inventory-status', methods=['GET', 'POST'])
@login_required
def inventory_status():
    form = UpdatePizzaDetailsForm()
    if form.validate_on_submit():
        pizza = Pizza.query.get(form.pizza_id.data)
        if pizza is not None:
            pizza.stock = form.stock.data
            pizza.toppings = form.toppings.data
            if form.name.data:
                pizza.name = form.name.data
            db.session.commit()
            flash('Inventory updated successfully!', 'success')
        else:
            flash('Pizza not found in inventory', 'danger')
    form.pizza_id.choices = [(pizza.id, pizza.name) for pizza in Pizza.query.all()]
    pizzas = Pizza.query.all()
    return render_template('inventory-status.html', title='Inventory Status', form=form, pizzas=pizzas)
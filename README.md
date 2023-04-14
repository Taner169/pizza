# Pizza Order Application

This is a simple web application for ordering pizzas, managing inventory and handling customer inquiries.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need Python 3.6 or later installed on your machine. You will also need the following Python packages:

- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login

### Installing

1. Clone the repository:
git clone https://github.com/taner169/pizza.git

2. Change into the project directory:
cd pizza-order-app

3. Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate

4. Install the required packages:
pip install -r requirements.txt

5. Run the application:
flask run


6. Open your browser and go to `http://localhost:5000` to access the application.

## Application Structure

The main files and folders in this application are:

- `app.py`: The main application file.
- `database.py`: Database configuration and initialization.
- `forms.py`: Contains the WTForms for user registration, login, and various other forms.
- `models.py`: Contains the SQLAlchemy models for the database tables.
- `templates`: Contains the Jinja2 templates for rendering the HTML pages.
- `static`: Contains the static files, such as CSS, JavaScript, and images.

## Forms

The application includes the following forms:

- `RegistrationForm`: For user registration.
- `LoginForm`: For user login.
- `ContactForm`: For submitting customer inquiries.
- `OrderForm`: For placing pizza orders.
- `AddPizzaForm`: For adding new pizza types to the menu.
- `UpdateInventoryForm`: For updating inventory.
- `RemovePizzaForm`: For removing pizzas from the menu.
- `UpdatePizzaDetailsForm`: For updating pizza details, such as toppings and stock.

## Models

The application includes the following models:

- `Pizza`: Represents a pizza with name, price, size, toppings, and stock.
- `User`: Represents a user with username, email, and password.
- `Contact`: Represents a customer inquiry with name, email, subject, and message.
- `Order`: Represents a pizza order with name, email, pizza_id, pizza_size, and price.
- `InventoryItem`: Represents an inventory item with name and stock.
- `Employee`: Represents an employee.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

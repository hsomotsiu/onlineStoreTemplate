#!/usr/bin/env python3

from authentication.auth_tools import login_pipeline, update_passwords, hash_password
from database.db import Database
from flask import Flask, render_template, request
from core.session import Sessions


app = Flask(__name__)
HOST, PORT = 'localhost', 8080
global username, products, reviews, db, sessions
username = 'default'
db = Database('database/store_records.db')
products = db.get_full_inventory()
reviews = db.get_all_reviews()
sessions = Sessions()
sessions.add_new_session(username, db)


@app.route('/')
def index_page():
    """
    Renders the index page when the user is at the `/` endpoint, passing along default flask variables.

    args:
        - None

    returns:
        - None
    """
    return render_template('index.html', username=username, products=products, sessions=sessions)

@app.route('/admin_dashboard')
def admin_dashboard():
    reviews = db.get_all_reviews()
    return render_template('admin/admin_dashboard.html', reviews=reviews)

@app.route('/login')
def login_page():
    """
    Renders the login page when the user is at the `/login` endpoint.

    args:
        - None

    returns:
        - None
    """
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def login():
    """
    Renders the home page when the user is at the `/home` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - sessions: adds a new session to the sessions object

    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_pipeline(username, password):
            sessions.add_new_session(username, db)
            return render_template('home.html', products=products, sessions=sessions)
        elif username == 'admin':
            return render_template('admin/admin_home.html', products=products)
        else:
            print(f"Incorrect username ({username}) or password ({password}).")
            return render_template('index.html')
    else:
        # Handle the GET request (render the home page)
        return render_template('home.html', products=products, sessions=sessions)

@app.route('/register')
def register_page():
    """
    Renders the register page when the user is at the `/register` endpoint.

    args:
        - None

    returns:
        - None
    """
    
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    """
    Renders the index page when the user is at the `/register` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - passwords.txt: adds a new username and password combination to the file
        - database/store_records.db: adds a new user to the database
    """
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    salt, key = hash_password(password)
    update_passwords(username, key, salt)
    db.insert_user(username, key, email, first_name, last_name)
    return render_template('index.html')

@app.route('/reset_password')
def reset_password_page():
    return render_template('reset_password.html')

@app.route('/reset_password', methods=['POST'])
def reset_password():
    username = request.form['username']
    new_password = request.form['new_password']
    db.set_password_hash(new_password, username)
    return render_template('login.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Renders the checkout page when the user is at the `/checkout` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - sessions: adds items to the user's cart
    """
    order = {}
    user_session = sessions.get_session(username)
    for item in products:
        print(f"item ID: {item['id']}")
        if request.form[str(item['id'])] > '0':
            count = request.form[str(item['id'])]
            order[item['item_name']] = count
            user_session.add_new_item(
                item['id'], item['item_name'], item['price'], count)

    user_session.submit_cart()

    return render_template('checkout.html', order=order, sessions=sessions, total_cost=user_session.total_cost)

@app.route('/order', methods=['GET'])
def ordernow():
    bakeries = get_bakeries()
    return render_template('ordernow.html', bakeries=bakeries)

# Add the get_bakeries() function
def get_bakeries():
    # Replace this with your actual database query to get bakery options
    # For simplicity, we'll define the items and prices manually for now
    return {
        "cakes": [
            {"name": "Fruit Sponge Cake", "price": 30.0},
            {"name": "Flan", "price": 20.0},
            {"name": "Ube Honeycomb", "price": 20.0},
            {"name": "Customized Rectangle", "price": 40.0},
            {"name": "Customized Heart", "price": 50.0},
            {"name": "Customized Round", "price": 40.0}
        ],
        "cupcakes": [
            {"name": "Pink cupcakes with marble cream cheese frosting", "price": 20.0},
            {"name": "Chocolate cupcakes with sprinkles", "price": 15.0}
        ],
        "breads": [
            {"name": "Milk Bread", "price": 5.0},
            {"name": "French Bread", "price": 4.0}
        ]
    }

# Modify the /place_order route
@app.route('/place_order', methods=['POST'])
def place_order():
    # Retrieve the form data from the submitted order
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    pick_up_date = request.form['pickUpDate']
    customization_note = request.form['customizationNote']

    # Retrieve the item price from the database
    bakery_items = get_bakeries()
    total_price = 0.0

    # Process the first bakery selection
    selected_bakery1 = request.form['selectBakery1']
    quantity1 = int(request.form['quantity1'])
    for category, items in bakery_items.items():
        for item in items:
            if item["name"] == selected_bakery1:
                total_price += item["price"] * quantity1
                break

    # Process the second bakery selection (if any)
    selected_bakery2 = request.form.get('selectBakery2')  # Use get() with default value None
    if selected_bakery2:
        quantity2 = int(request.form['quantity2'])
        for category, items in bakery_items.items():
            for item in items:
                if item["name"] == selected_bakery2:
                    total_price += item["price"] * quantity2
                    break

    # Process the third bakery selection (if any)
    selected_bakery3 = request.form.get('selectBakery3')  # Use get() with default value None
    if selected_bakery3:
        quantity3 = int(request.form['quantity3'])
        for category, items in bakery_items.items():
            for item in items:
                if item["name"] == selected_bakery3:
                    total_price += item["price"] * quantity3
                    break

    # Calculate the tax (2.00%)
    tax = 0.02 * total_price

    # Calculate the final total price with tax
    total_price_with_tax = total_price + tax

    # Render the totalprice.html template with the order details and total price
    return render_template('totalprice.html', first_name=first_name, last_name=last_name, email=email, phone=phone,
                           pick_up_date=pick_up_date, customization_note=customization_note,
                           selected_bakery1=selected_bakery1, quantity1=quantity1,
                           selected_bakery2=selected_bakery2, quantity2=quantity2 if selected_bakery2 else None,
                           selected_bakery3=selected_bakery3, quantity3=quantity3 if selected_bakery3 else None,
                           subtotal=total_price, tax=tax, total_price=total_price_with_tax)


@app.route('/menu')
def menu_page():
    """
    Renders the menu page when the user is at the `/menu` endpoint.

    args:
        - None

    returns:
        - None
    """
    return render_template('menu.html', products=products, sessions=sessions)

@app.route('/review', methods=['POST'])
def review():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    review = request.form['review']
    db.insert_new_review(first_name, last_name, email, review)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)

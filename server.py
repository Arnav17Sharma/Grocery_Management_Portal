from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from sql_connection import get_sql_connection
import mysql.connector
import json
import os
import cloudinary
import cloudinary.uploader

# --- DAO Imports ---
import products_dao
import orders_dao
import uom_dao
import users_dao # <-- NEW IMPORT

app = Flask(__name__)

# --- Secret Key Configuration (IMPORTANT) ---
# Add a SECRET_KEY to your .env file for session security
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "a-fallback-secret-key-if-not-set")

# --- Cloudinary Configuration ---
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = True
)

connection = get_sql_connection()

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
# If a user tries to access a protected page, redirect them to the 'login' view.
login_manager.login_view = 'login'

# --- User Model for Flask-Login ---
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.password_hash = user_data['password_hash']

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- User Loader for Flask-Login ---
# This function is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    user_data = users_dao.get_user_by_id(connection, user_id)
    if user_data:
        return User(user_data)
    return None

# --- NEW AUTHENTICATION ROUTES ---

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('get_all_orders'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('get_all_orders')) # Redirect to main page if already logged in

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = users_dao.get_user_by_email(connection, email)

        # Check if user exists and password is correct
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data)
            login_user(user) # Log the user in and create a session
            return redirect(url_for('get_all_orders'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('get_all_orders'))

    if request.method == 'POST':
        user_data = {
            'email': request.form['email'],
            'username': request.form['username'],
            'password': request.form['password']
        }
        
        # Check if user already exists
        if users_dao.get_user_by_email(connection, user_data['email']):
            flash('An account with this email already exists.', 'warning')
            return redirect(url_for('register'))
        
        # Create user
        user_id = users_dao.create_user(connection, user_data)
        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'danger')

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --- PROTECTED APPLICATION ROUTES ---

@app.route('/getUOM', methods=['GET'])
@login_required # <-- PROTECTED
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# --- MODIFIED ROUTE: Only shows the product list ---
@app.route('/getProducts') # Methods list removed, now only accepts GET
@login_required 
def get_products():
    response = products_dao.get_all_products(connection)
    # This route now ONLY displays the manage-product page.
    return render_template("manage-product.html", response=response, len=len(response), user=current_user)

# --- NEW ROUTE: For adding a new product ---
@app.route('/addProduct', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        # This is the logic we moved from the old get_products route
        image_url = None
        if 'product_image' in request.files and request.files['product_image'].filename != '':
            image_file = request.files['product_image']
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result['secure_url']

        request_payload = {
            "product_name": request.form['prod_name'],
            "uom_id": request.form['uom_id'],
            "price_per_unit": request.form['price_per_unit'],
            "image_url": image_url
        }
        products_dao.insert_new_product(connection, request_payload)
        # After saving, redirect back to the product list
        return redirect(url_for('get_products'))

    # On a GET request, render the form to add a new product
    return render_template("new_product.html")

@app.route('/getOrders', methods=['GET', 'POST'])
@login_required # <-- PROTECTED
def get_all_orders():
    if request.method == 'POST':
        data = request.form['data']
        result = list(eval(data))
        customer_name = request.form['customer_name']
        total = request.form['total']
        request_payload = {
            "customer_name": customer_name,
            "grand_total": total,
            "order_details": []
        }
        for i in result:
            request_payload['order_details'].append(i)
        
        orders_dao.insert_order(connection, request_payload)
    
    response = orders_dao.get_all_orders(connection)
    # Pass the current_user to the template
    return render_template("index.html", response=response, user=current_user)

@app.route('/insertOrder', methods=['GET', 'POST'])
@login_required # <-- PROTECTED
def insert_order():
    response = products_dao.get_all_products(connection)
    # Pass the current_user to the template
    return render_template("new_order.html", response=response, len=len(response), user=current_user)

@app.route('/deleteProduct', methods=['POST'])
@login_required # <-- PROTECTED
def delete_product():
    if request.method == 'POST':
        prod_id = request.form['product_id']
        products_dao.delete_product(connection, prod_id)
        # No need to return JSON if you are just redirecting
        return redirect('/getProducts')

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(debug=True)
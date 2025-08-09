
from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import or_
import os
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from datetime import datetime, timedelta
from src.controllers.customers import db, Customer, Customeridentification
from src.controllers.employees import db, Employees, Employeeidentification
from src.controllers.rooms import db, Room
from src.controllers.login_helpers import LoginUser
from src.controllers.hotels import Hotels
from src.controllers.hotel_chains import Hotelchains
from src.controllers.rentings import Rentings

from src.database.database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:Stefzora003@localhost/CSI2132-Hotel-Project'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-dev-key')

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'customer_login'
login_manager.init_app(app)

from src.controllers.customers import customers_bp
from src.controllers.employees import employees_bp
from src.controllers.hotel_chains import hotel_chains_bp
from src.controllers.hotels import hotels_bp
from src.controllers.rentings import rentings_bp
from src.controllers.rooms import rooms_bp

app.register_blueprint(hotel_chains_bp, url_prefix='/api')
app.register_blueprint(hotels_bp, url_prefix='/api')
app.register_blueprint(rooms_bp, url_prefix='/api')
app.register_blueprint(customers_bp, url_prefix='/api')
app.register_blueprint(rentings_bp, url_prefix='/api')
app.register_blueprint(employees_bp, url_prefix='/api')

@login_manager.user_loader
def load_user(user_id):
    role, real_id = user_id.split(':')
    if role == 'customer':
        return LoginUser(real_id, 'customer')
    elif role == 'employee':
        return LoginUser(real_id, 'employee')
    return None

@app.route('/')
def hello_world(): 
    return render_template("index.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.', category='success')
    return render_template("index.html")

@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'signup':
            full_name = request.form.get('full_name')
            address = request.form.get('address')
            content = request.form.get('content')
            driver_license = request.form.get('driver_license')
            driver_license_confirm = request.form.get('driver_license_confirm')
            registration_date = datetime.utcnow()

            existing_customer = Customer.query.filter_by(full_name=full_name, address=address).first()
            if existing_customer:
                flash('You are already an existing customer!', category='error')
                return redirect(url_for('customer_login'))
        
            if len(full_name) < 4:
                flash('Full name must be greater than 3 characters', category='error')
            elif len(address) < 6:
                flash('Must be a valid address', category='error')
            elif driver_license != driver_license_confirm:
                flash('Drivers License numbers don\'t match.', category='error')
            elif not full_name or not address or not driver_license or not driver_license_confirm:
                flash('Please enter all fields.', category='error')
            else:
                new_customer = Customer(full_name=full_name, address=address)
                db.session.add(new_customer)
                db.session.commit() 

                new_customer_identification = Customeridentification(
                    id_type='email',
                    content=content,
                    customer_id=new_customer.id,
                    driver_license=driver_license
                )
                db.session.add(new_customer_identification)
                db.session.commit()

                flash('New customer profile created successfully!', category='success')
                return redirect(url_for('customer_dashboard'))
    
        elif action == 'login':
            content = request.form.get('content_submit')
            driver_license = request.form.get('driver_license_submit')

            identification = Customeridentification.query.filter_by(content=content, driver_license=driver_license).first()
            if identification:
                login_user(LoginUser(identification.customer_id, 'customer'))
                flash("Logged in successfully as customer.", category="success")
                return redirect(url_for('customer_dashboard'))
            else:
                flash("Login failed. Check your credentials and try again.", category="error")

    return render_template("customer_login.html")

@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        content = request.form.get('content')
        password = request.form.get('password')

        identification = Employeeidentification.query.filter_by(content=content, password=password).first()
        if identification:
            login_user(LoginUser(identification.employee_id, 'employee'))
            flash('Logged in successfully as employee.', category='success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login failed. Check your credentials.', category='error')
    
    return render_template('employee_login.html')


@app.route('/customer_dashboard', methods=['GET'])
@login_required
def customer_dashboard():
    # Check if filters are submitted
    if request.args:
        hotel_chain_ids = request.args.getlist('name')
        city_ids = request.args.getlist('city')
        view_types = request.args.getlist('view_types')
        star_rating = request.args.get('star_rating')
        max_price = request.args.get('price')
        capacity = request.args.get('capacity')

        query = """
            SELECT r.room_number, r.price, r.view_types, r.capacity, r.amenities, r.is_extendable,
                   h.name AS hotel_name, h.star_rating, h.address AS hotel_address,
                   hc.name AS chain_name
            FROM rooms r
            JOIN hotels h ON r.hotel_id = h.id
            JOIN hotelchains hc ON h.hotel_chain_id = hc.id
            WHERE r.is_available = TRUE
        """
        params = []

        if hotel_chain_ids:
            query += f" AND h.hotel_chain_id IN ({','.join(['%s'] * len(hotel_chain_ids))})"
            params.extend(hotel_chain_ids)

        if city_ids:
            query += f" AND h.city IN ({','.join(['%s'] * len(city_ids))})"
            params.extend(city_ids)

        if view_types:
            placeholders = ','.join(['%s'] * len(view_types))
            query += f" AND (r.view_types IN ({placeholders}) OR r.view_types = 'None')"
            params.extend(view_types)


        if star_rating:
            query += " AND h.star_rating >= %s"
            params.append(star_rating)

        if max_price:
            query += " AND r.price <= %s"
            params.append(max_price)

        if capacity:
            query += " AND r.capacity >= %s"
            params.append(capacity)

        result = db.engine.execute(query, tuple(params))
        rooms = [dict(row) for row in result]

        return render_template("results.html", rooms=rooms)

    # No filters submitted — just show dashboard with filter form
    return render_template("customer_dashboard.html")

@app.route('/admin_dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    employee_id = current_user.id

    chain_query = """
        SELECT hc.id
        FROM employees e
        JOIN hotels h ON e.hotel_id = h.id
        JOIN hotelchains hc ON h.hotel_chain_id = hc.id
        WHERE e.id = %s
    """
    chain_result = db.engine.execute(chain_query, (employee_id,))
    chain_row = chain_result.fetchone()

    if not chain_row:
        flash("Could not determine your hotel chain.", category="error")
        return redirect(url_for("home"))

    hotel_chain_id = chain_row[0]

    rooms_query = """
        SELECT r.id, r.room_number, r.capacity, r.price, r.is_extendable, r.view_types, r.amenities,
               h.name AS hotel_name, h.star_rating
        FROM rooms r
        JOIN hotels h ON r.hotel_id = h.id
        WHERE h.hotel_chain_id = %s
    """
    rooms_result = db.engine.execute(rooms_query, (hotel_chain_id,))
    rooms = [dict(row) for row in rooms_result]

    return render_template("admin_dashboard.html", rooms=rooms)


@app.route('/results')
@login_required
def results():
    rooms = Room.query.all()
    return render_template('results.html', rooms=rooms)

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if request.method == "POST":
        room_id = request.form.get("room_id")
        return render_template("checkout.html", room_id=room_id)

    flash("Please select a room first.", category="error")
    return redirect(url_for("customer_dashboard"))

@app.route("/admin_results", methods=["GET", "POST"])
@login_required
def admin_results():
    room_id = request.form.get('room_id')

    print(room_id)
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'signup':
            full_name = request.form.get('full_name')
            address = request.form.get('address')
            content = request.form.get('content')
            driver_license = request.form.get('driver_license')
            registration_date = datetime.utcnow()

            existing_customer = Customer.query.filter_by(full_name=full_name, address=address).first()
            if existing_customer:
                flash('This customer already exists!', category='error')
                return redirect(url_for('admin_results'))
            else:
                new_customer = Customer(full_name=full_name, address=address)
                db.session.add(new_customer)
                db.session.commit() 

                new_customer_identification = Customeridentification(
                    id_type='email',
                    content=content,
                    customer_id=new_customer.id,
                    driver_license=driver_license
                )
                db.session.add(new_customer_identification)
                db.session.commit()

                flash('New customer registered successfully!', category='success')
                return redirect(url_for('checkout'))
    
        elif action == 'login':
            content = request.form.get('content_submit')
            driver_license = request.form.get('driver_license_submit')

            identification = Customeridentification.query.filter_by(content=content, driver_license=driver_license).first()
            if identification:
                flash("Customer successfully identified!", category="success")
                customer_id = identification.customer_id
                return redirect(url_for('checkout'))
            else:
                flash("Customer does not exist.", category="error")

    return render_template("admin_results.html")

@app.route("/confirm_booking", methods=["GET", "POST"])
@login_required
def confirm_booking():
    room_id = request.form.get("room_id")
    check_in = request.form.get("check_in_date")
    check_out = request.form.get("check_out_date")
    credit_card = request.form.get("credit_card")

    print(current_user)

    if current_user != 'employee':
        employee_id = 0
        customer_id = current_user.id
    else:
        employee_id = current_user.id

    # Validate dates
    if check_out <= check_in:
        flash("Check-out must be after check-in", category="error")
        return redirect(url_for("checkout"))

    # Insert into Rentings table
    query = """
        INSERT INTO Rentings (was_booked, check_in_date, check_out_date, payment_status, customer_id, room_id, employee_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    db.engine.execute(query, (True, check_in, check_out, 'paid', customer_id, room_id, employee_id))

    flash("Booking confirmed!", "success")
    if current_user != 'employee':
        return redirect(url_for("customer_dashboard"))
    else:
        return redirect(url_for("admin_dashboard"))

if __name__ == '__main__':
    app.run(debug=True)


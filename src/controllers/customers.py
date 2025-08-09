from flask import Blueprint, request, jsonify
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

customers_bp = Blueprint('customers', __name__)

# Create a new customer
@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    query = """
        INSERT INTO Customers (full_name, address, registration_date)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (data['full_name'], data['address'], data['registration_date']))
    customer_id = result.fetchone()[0]
    return jsonify({"message": "Customer created", "id": customer_id}), 201

# Get all customers
@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    query = "SELECT id, full_name, address, registration_date FROM Customers;"
    result = db.engine.execute(query)
    customers = [dict(row) for row in result]
    return jsonify(customers), 200

# Get a specific customer by ID
@customers_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    query = "SELECT id, full_name, address, registration_date FROM Customers WHERE id = %s;"
    result = db.engine.execute(query, (id,))
    customer = result.fetchone()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(dict(customer)), 200

# Update a customer
@customers_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    query = """
        UPDATE Customers
        SET full_name = %s, address = %s, registration_date = %s
        WHERE id = %s;
    """
    db.engine.execute(query, (data['full_name'], data['address'], data['registration_date'], id))
    return jsonify({"message": "Customer updated"}), 200

# Delete a customer
@customers_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    query = "DELETE FROM Customers WHERE id = %s;"
    db.engine.execute(query, (id,))
    return jsonify({"message": "Customer deleted"}), 200

# Create a new customer identification
@customers_bp.route('/customers/<int:customer_id>/identifications', methods=['POST'])
def create_customer_identification(customer_id):
    data = request.get_json()
    query = """
        INSERT INTO CustomerIdentification (id_type, content, customer_id, driver_license)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (data['id_type'], data['content'], customer_id, data['driver_license']))
    identification_id = result.fetchone()[0]
    return jsonify({"message": "Customer identification created", "id": identification_id}), 201

# Get all identifications for a customer
@customers_bp.route('/customers/<int:customer_id>/identifications', methods=['GET'])
def get_customer_identifications(customer_id):
    query = "SELECT id, id_type, content, customer_id FROM CustomerIdentification WHERE customer_id = %s;"
    result = db.engine.execute(query, (customer_id,))
    identifications = [dict(row) for row in result]
    return jsonify(identifications), 200

# Get a specific identification by ID
@customers_bp.route('/customers/<int:customer_id>/identifications/<int:id>', methods=['GET'])
def get_customer_identification(customer_id, id):
    query = "SELECT id, id_type, content, customer_id FROM CustomerIdentification WHERE id = %s AND customer_id = %s;"
    result = db.engine.execute(query, (id, customer_id))
    identification = result.fetchone()
    if not identification:
        return jsonify({"error": "Identification not found"}), 404
    return jsonify(dict(identification)), 200

# Update a customer identification
@customers_bp.route('/customers/<int:customer_id>/identifications/<int:id>', methods=['PUT'])
def update_customer_identification(customer_id, id):
    data = request.get_json()
    query = """
        UPDATE CustomerIdentification
        SET id_type = %s, content = %s
        WHERE id = %s AND customer_id = %s;
    """
    db.engine.execute(query, (data.get('id_type'), data.get('content'), id, customer_id))
    return jsonify({"message": "Customer identification updated"}), 200

# Delete a customer identification
@customers_bp.route('/customers/<int:customer_id>/identifications/<int:id>', methods=['DELETE'])
def delete_customer_identification(customer_id, id):
    query = "DELETE FROM CustomerIdentification WHERE id = %s AND customer_id = %s;"
    db.engine.execute(query, (id, customer_id))
    return jsonify({"message": "Customer identification deleted"}), 200

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    registration_date = db.Column(db.DateTime(timezone=True), default=func.now())

class Customeridentification(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    driver_license = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
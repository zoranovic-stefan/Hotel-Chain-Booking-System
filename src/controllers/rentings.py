from flask import Blueprint, request, jsonify
from src.database.database import db

rentings_bp = Blueprint('rentings', __name__)

# Create a new renting
@rentings_bp.route('/rentings', methods=['POST'])
def create_renting():
    data = request.get_json()
    query = """
        INSERT INTO Rentings (was_booked, check_in_date, check_out_date, payment_status, customer_id, room_id, employee_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (
        data['was_booked'], data['check_in_date'], data['check_out_date'], data['payment_status'],
        data['customer_id'], data['room_id'], data['employee_id']
    ))
    renting_id = result.fetchone()[0]
    return jsonify({"message": "Renting created", "id": renting_id}), 201

# Get all rentings
@rentings_bp.route('/rentings', methods=['GET'])
def get_rentings():
    query = "SELECT id, was_booked, check_in_date, check_out_date, payment_status, customer_id, room_id, employee_id FROM Rentings;"
    result = db.engine.execute(query)
    rentings = [dict(row) for row in result]
    return jsonify(rentings), 200

# Get a specific renting by ID
@rentings_bp.route('/rentings/<int:id>', methods=['GET'])
def get_renting(id):
    query = "SELECT id, was_booked, check_in_date, check_out_date, payment_status, customer_id, room_id, employee_id FROM Rentings WHERE id = %s;"
    result = db.engine.execute(query, (id,))
    renting = result.fetchone()
    if not renting:
        return jsonify({"error": "Renting not found"}), 404
    return jsonify(dict(renting)), 200

# Update a renting
@rentings_bp.route('/rentings/<int:id>', methods=['PUT'])
def update_renting(id):
    data = request.get_json()
    query = """
        UPDATE Rentings
        SET was_booked = %s, check_in_date = %s, check_out_date = %s, payment_status = %s, customer_id = %s, room_id = %s, employee_id = %s
        WHERE id = %s;
    """
    db.engine.execute(query, (
        data.get('was_booked'), data.get('check_in_date'), data.get('check_out_date'), data.get('payment_status'),
        data.get('customer_id'), data.get('room_id'), data.get('employee_id'), id
    ))
    return jsonify({"message": "Renting updated"}), 200

# Delete a renting
@rentings_bp.route('/rentings/<int:id>', methods=['DELETE'])
def delete_renting(id):
    query = "DELETE FROM Rentings WHERE id = %s;"
    db.engine.execute(query, (id,))
    return jsonify({"message": "Renting deleted"}), 200

class Rentings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    was_booked = db.Column(db.Boolean)
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    payment_status = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    rooms_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
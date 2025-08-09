from flask import Blueprint, request, jsonify
#from src.database.database import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

employees_bp = Blueprint('employees', __name__)

# Create a new employee
@employees_bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    query = """
        INSERT INTO Employees (full_name, address, role, hotel_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (data['full_name'], data['address'], data['role'], data['hotel_id']))
    employee_id = result.fetchone()[0]
    return jsonify({"message": "Employee created", "id": employee_id}), 201

# Get all employees
@employees_bp.route('/employees', methods=['GET'])
def get_employees():
    query = "SELECT id, full_name, address, role, hotel_id FROM Employees;"
    result = db.engine.execute(query)
    employees = [dict(row) for row in result]
    return jsonify(employees), 200

# Get a specific employee by ID
@employees_bp.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    query = "SELECT id, full_name, address, role, hotel_id FROM Employees WHERE id = %s;"
    result = db.engine.execute(query, (id,))
    employee = result.fetchone()
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(dict(employee)), 200


# Update an employee
@employees_bp.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    query = """
        UPDATE Employees
        SET full_name = %s, address = %s, role = %s, hotel_id = %s
        WHERE id = %s;
    """
    db.engine.execute(query, (
        data.get('full_name'), data.get('address'), data.get('role'), data.get('hotel_id'), id
    ))
    return jsonify({"message": "Employee updated"}), 200

# Delete an employee
@employees_bp.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    query = "DELETE FROM Employees WHERE id = %s;"
    db.engine.execute(query, (id,))
    return jsonify({"message": "Employee deleted"}), 200

# Create a new employee identification
@employees_bp.route('/employees/<int:employee_id>/identifications', methods=['POST'])
def create_employee_identification(employee_id):
    data = request.get_json()
    query = """
        INSERT INTO EmployeeIdentification (id_type, content, employee_id)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (data['id_type'], data['content'], employee_id))
    identification_id = result.fetchone()[0]
    return jsonify({"message": "Employee identification created", "id": identification_id}), 201

# Get all identifications for an employee
@employees_bp.route('/employees/<int:employee_id>/identifications', methods=['GET'])
def get_employee_identifications(employee_id):
    query = "SELECT id, id_type, content, employee_id FROM EmployeeIdentification WHERE employee_id = %s;"
    result = db.engine.execute(query, (employee_id,))
    identifications = [dict(row) for row in result]
    return jsonify(identifications), 200

# Get a specific identification by ID
@employees_bp.route('/employees/<int:employee_id>/identifications/<int:id>', methods=['GET'])
def get_employee_identification(employee_id, id):
    query = "SELECT id, id_type, content, employee_id FROM EmployeeIdentification WHERE id = %s AND employee_id = %s;"
    result = db.engine.execute(query, (id, employee_id))
    identification = result.fetchone()
    if not identification:
        return jsonify({"error": "Identification not found"}), 404
    return jsonify(dict(identification)), 200

# Update an employee identification
@employees_bp.route('/employees/<int:employee_id>/identifications/<int:id>', methods=['PUT'])
def update_employee_identification(employee_id, id):
    data = request.get_json()
    query = """
        UPDATE EmployeeIdentification
        SET id_type = %s, content = %s
        WHERE id = %s AND employee_id = %s;
    """
    db.engine.execute(query, (data.get('id_type'), data.get('content'), id, employee_id))
    return jsonify({"message": "Employee identification updated"}), 200

# Delete an employee identification
@employees_bp.route('/employees/<int:employee_id>/identifications/<int:id>', methods=['DELETE'])
def delete_employee_identification(employee_id, id):
    query = "DELETE FROM EmployeeIdentification WHERE id = %s AND employee_id = %s;"
    db.engine.execute(query, (id, employee_id))
    return jsonify({"message": "Employee identification deleted"}), 200

class Employees(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))

class Employeeidentification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

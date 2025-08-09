import sys
from flask import Blueprint, request, jsonify
from src.database.database import db
from flask_sqlalchemy import SQLAlchemy

rooms_bp = Blueprint('rooms', __name__)
db = SQLAlchemy()

# Create a new room
@rooms_bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    query = """
        INSERT INTO Rooms (room_number, capacity, price, is_extendable, view_types, amenities, problems, hotel_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (
        data['room_number'], data['capacity'], data['price'], data['is_extendable'],
        data.get('view_types'), data['amenities'], data.get('problems'), data['hotel_id']
    ))
    room_id = result.fetchone()[0]
    return jsonify({"message": "Room created", "id": room_id}), 201

# Get all rooms
@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
   
    query = "SELECT id, room_number, capacity, price, is_extendable, view_types, amenities, problems, hotel_id FROM Rooms;"
    result = db.engine.execute(query)
    rooms = [dict(row) for row in result]
    return jsonify(rooms), 200

# Get a specific room by ID
@rooms_bp.route('/rooms/<int:id>', methods=['GET'])
def get_room(id):
    query = "SELECT id, room_number, capacity, price, is_extendable, view_types, amenities, problems, hotel_id FROM Rooms WHERE id = %s;"
    result = db.engine.execute(query, (id,))
    room = result.fetchone()
    if not room:
        return jsonify({"error": "Room not found"}), 404
    return jsonify(dict(room)), 200

# Update a room
@rooms_bp.route('/rooms/<int:id>', methods=['PUT'])
def update_room(id):
    data = request.get_json()
    query = """
        UPDATE Rooms
        SET room_number = %s, capacity = %s, price = %s, is_extendable = %s, view_types = %s, amenities = %s, problems = %s, hotel_id = %s
        WHERE id = %s;
    """
    db.engine.execute(query, (
        data.get('room_number'), data.get('capacity'), data.get('price'), data.get('is_extendable'),
        data.get('view_types'), data.get('amenities'), data.get('problems'), data.get('hotel_id'), id
    ))
    return jsonify({"message": "Room updated"}), 200

# Delete a room
@rooms_bp.route('/rooms/<int:id>', methods=['DELETE'])
def delete_room(id):
    query = "DELETE FROM Rooms WHERE id = %s;"
    db.engine.execute(query, (id,))
    return jsonify({"message": "Room deleted"}), 200

# find all rooms with the right destination, capacity that are not rented. 
@rooms_bp.route('/rooms/available', methods=['GET'])
def get_available_rooms():
 
    data = request.get_json()
    destination = data.get('destination')
    capacity = data.get('capacity')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
   
    query = """ 
        SELECT * FROM Rooms
        WHERE hotel_id IN (SELECT id FROM Hotels WHERE destination ILIKE %s)
        AND capacity >= %s AND id NOT IN (SELECT room_id FROM Rentings WHERE check_in_date <= %s AND check_out_date >= %s);
    """
    result = db.engine.execute(query, (f"%{destination}%", capacity, check_in, check_out))
    rooms = [dict(row) for row in result]
    return jsonify(rooms), 200

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_extendable = db.Column(db.Boolean, nullable=False)
    view_types = db.Column(db.String(100))
    amenities = db.Column(db.String(200), nullable=False)
    problems = db.Column(db.String(200))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id', ondelete='CASCADE'), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
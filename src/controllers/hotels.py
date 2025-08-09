from flask import Blueprint, request, jsonify
from src.database.database import db
from src.controllers.hotel_chains import db, Hotelchains

hotels_bp = Blueprint('hotels', __name__)

# Create a new hotel
@hotels_bp.route('/hotels', methods=['POST'])
def create_hotel():
    data = request.get_json()
    query = """
        INSERT INTO Hotels (name, address, star_rating, hotel_chain_id, city)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (data['name'], data['address'], data['star_rating'], data['hotel_chain_id']))
    hotel_id = result.fetchone()[0]
    return jsonify({"message": "Hotel created", "id": hotel_id}), 201

# Get all hotels
@hotels_bp.route('/hotels', methods=['GET'])
def get_hotels():
    query = "SELECT id, name, address, star_rating, hotel_chain_id FROM Hotels;"
    result = db.engine.execute(query)
    hotels = [dict(row) for row in result]
    return jsonify(hotels), 200

# Get a specific hotel by ID
@hotels_bp.route('/hotels/<int:id>', methods=['GET'])
def get_hotel(id):
    query = "SELECT id, name, address, star_rating, hotel_chain_id FROM Hotels WHERE id = %s;"
    result = db.engine.execute(query, (id,))
    hotel = result.fetchone()
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    return jsonify(dict(hotel)), 200

# Update a hotel
@hotels_bp.route('/hotels/<int:id>', methods=['PUT'])
def update_hotel(id):
    data = request.get_json()
    query = """
        UPDATE Hotels
        SET name = %s, address = %s, star_rating = %s, hotel_chain_id = %s
        WHERE id = %s;
    """
    db.engine.execute(query, (data['name'], data['address'], data['star_rating'], data['hotel_chain_id'], id))
    return jsonify({"message": "Hotel updated"}), 200

# Delete a hotel
@hotels_bp.route('/hotels/<int:id>', methods=['DELETE'])
def delete_hotel(id):
    query = "DELETE FROM Hotels WHERE id = %s;"
    db.engine.execute(query, (id,))
    return jsonify({"message": "Hotel deleted"}), 200

# Create a new hotel contact
@hotels_bp.route('/hotels/<int:hotel_id>/contacts', methods=['POST'])
def create_hotel_contact(hotel_id):
    data = request.get_json()
    query = """
        INSERT INTO HotelContact (hotel_id, type, content)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (hotel_id, data['type'], data['content']))
    contact_id = result.fetchone()[0]
    return jsonify({"message": "Hotel contact created", "id": contact_id}), 201

# Get all contacts for a hotel
@hotels_bp.route('/hotels/<int:hotel_id>/contacts', methods=['GET'])
def get_hotel_contacts(hotel_id):
    query = "SELECT id, hotel_id, type, content FROM HotelContact WHERE hotel_id = %s;"
    result = db.engine.execute(query, (hotel_id,))
    contacts = [dict(row) for row in result]
    return jsonify(contacts), 200

# Get a specific contact by ID
@hotels_bp.route('/hotels/<int:hotel_id>/contacts/<int:id>', methods=['GET'])
def get_hotel_contact(hotel_id, id):
    query = "SELECT id, hotel_id, type, content FROM HotelContact WHERE id = %s AND hotel_id = %s;"
    result = db.engine.execute(query, (id, hotel_id))
    contact = result.fetchone()
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    return jsonify(dict(contact)), 200

# Update a hotel contact
@hotels_bp.route('/hotels/<int:hotel_id>/contacts/<int:id>', methods=['PUT'])
def update_hotel_contact(hotel_id, id):
    data = request.get_json()
    query = """
        UPDATE HotelContact
        SET type = %s, content = %s
        WHERE id = %s AND hotel_id = %s;
    """
    db.engine.execute(query, (data.get('type'), data.get('content'), id, hotel_id))
    return jsonify({"message": "Hotel contact updated"}), 200

# Delete a hotel contact
@hotels_bp.route('/hotels/<int:hotel_id>/contacts/<int:id>', methods=['DELETE'])
def delete_hotel_contact(hotel_id, id):
    query = "DELETE FROM HotelContact WHERE id = %s AND hotel_id = %s;"
    db.engine.execute(query, (id, hotel_id))
    return jsonify({"message": "Hotel contact deleted"}), 200

class Hotels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    star_rating = db.Column(db.Integer)
    hotel_chain_id = db.Column(db.Integer, db.ForeignKey('hotelchains.id'), nullable=False)
    city = db.Column(db.String(50))
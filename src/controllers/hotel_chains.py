from flask import Blueprint, request, jsonify
from src.database.database import db

hotel_chains_bp = Blueprint('hotel_chains', __name__)

# Create a new hotel chain
@hotel_chains_bp.route('/hotel_chains', methods=['POST'])
def create_hotel_chain():
    data = request.get_json()
    query = """
        INSERT INTO HotelChains (name, office_address)
        VALUES (%s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (data['name'], data['office_address']))
    hotel_chain_id = result.fetchone()[0]
    return jsonify({"message": "Hotel chain created", "id": hotel_chain_id}), 201

# Get all hotel chains
@hotel_chains_bp.route('/hotel_chains', methods=['GET'])
def get_hotel_chains():
    query = "SELECT id, name, office_address FROM HotelChains;"
    result = db.engine.execute(query)
    hotel_chains = [dict(row) for row in result]
    return jsonify(hotel_chains), 200

# Get a specific hotel chain by ID
@hotel_chains_bp.route('/hotel_chains/<int:id>', methods=['GET'])
def get_hotel_chain(id):
    query = "SELECT id, name, office_address FROM HotelChains WHERE id = %s;"
    result = db.engine.execute(query, (id,))
    hotel_chain = result.fetchone()
    if not hotel_chain:
        return jsonify({"error": "Hotel chain not found"}), 404
    return jsonify(dict(hotel_chain)), 200

# Update a hotel chain
@hotel_chains_bp.route('/hotel_chains/<int:id>', methods=['PUT'])
def update_hotel_chain(id):
    data = request.get_json()
    query = """
        UPDATE HotelChains
        SET name = %s, office_address = %s
        WHERE id = %s;
    """
    db.engine.execute(query, (data['name'], data['office_address'], id))
    return jsonify({"message": "Hotel chain updated"}), 200

# Delete a hotel chain
@hotel_chains_bp.route('/hotel_chains/<int:id>', methods=['DELETE'])
def delete_hotel_chain(id):
    query = "DELETE FROM HotelChains WHERE id = %s;"
    db.engine.execute(query, (id,))
    return jsonify({"message": "Hotel chain deleted"}), 200


# Create a new hotel chain contact
@hotel_chains_bp.route('/hotel_chains/<int:hotel_chain_id>/contacts', methods=['POST'])
def create_hotel_chain_contact(hotel_chain_id):
    data = request.get_json()
    query = """
        INSERT INTO HotelChainContact (hotel_chain_id, type, content)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    result = db.engine.execute(query, (hotel_chain_id, data['type'], data['content']))
    contact_id = result.fetchone()[0]
    return jsonify({"message": "Hotel chain contact created", "id": contact_id}), 201

# Get all contacts for a hotel chain
@hotel_chains_bp.route('/hotel_chains/<int:hotel_chain_id>/contacts', methods=['GET'])
def get_hotel_chain_contacts(hotel_chain_id):
    query = "SELECT id, hotel_chain_id, type, content FROM HotelChainContact WHERE hotel_chain_id = %s;"
    result = db.engine.execute(query, (hotel_chain_id,))
    contacts = [dict(row) for row in result]
    return jsonify(contacts), 200

# Get a specific contact by ID
@hotel_chains_bp.route('/hotel_chains/<int:hotel_chain_id>/contacts/<int:id>', methods=['GET'])
def get_hotel_chain_contact(hotel_chain_id, id):
    query = "SELECT id, hotel_chain_id, type, content FROM HotelChainContact WHERE id = %s AND hotel_chain_id = %s;"
    result = db.engine.execute(query, (id, hotel_chain_id))
    contact = result.fetchone()
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    return jsonify(dict(contact)), 200

# Update a hotel chain contact
@hotel_chains_bp.route('/hotel_chains/<int:hotel_chain_id>/contacts/<int:id>', methods=['PUT'])
def update_hotel_chain_contact(hotel_chain_id, id):
    data = request.get_json()
    query = """
        UPDATE HotelChainContact
        SET type = %s, content = %s
        WHERE id = %s AND hotel_chain_id = %s;
    """
    db.engine.execute(query, (data.get('type'), data.get('content'), id, hotel_chain_id))
    return jsonify({"message": "Hotel chain contact updated"}), 200

# Delete a hotel chain contact
@hotel_chains_bp.route('/hotel_chains/<int:hotel_chain_id>/contacts/<int:id>', methods=['DELETE'])
def delete_hotel_chain_contact(hotel_chain_id, id):
    query = "DELETE FROM HotelChainContact WHERE id = %s AND hotel_chain_id = %s;"
    db.engine.execute(query, (id, hotel_chain_id))
    return jsonify({"message": "Hotel chain contact deleted"}), 200

class Hotelchains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    office_address = db.Column(db.String(200))
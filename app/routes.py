from flask import request, jsonify
from app.crud import create_note_in_db, update_note_in_db, delete_note_in_db
from app.utils import find_user_by_email, find_note_by_id

# API-Routen
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if find_user_by_email(data['email']):
        return jsonify({'error': 'User already exists'}), 400
    user_id = len(users_db) + 1
    users_db.append({
        'id': user_id,
        'name': data['name'],
        'email': data['email'],
        'password': data['password'],
        'admin': False
    })
    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = find_user_by_email(data['email'])
    if user and user['password'] == data['password']:
        return jsonify({'message': 'Login successful', 'session_token': 'mock_token'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    note_id = create_note_in_db(data)
    return jsonify({'message': 'Note created successfully', 'note_id': note_id}), 201

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = find_note_by_id(note_id)
    if note:
        return jsonify(note), 200
    return jsonify({'error': 'Note not found'}), 404

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.json
    if update_note_in_db(note_id, data):
        return jsonify({'message': 'Note updated successfully'}), 200
    return jsonify({'error': 'Note not found'}), 404

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    if delete_note_in_db(note_id):
        return jsonify({'message': 'Note deleted successfully'}), 200
    return jsonify({'error': 'Note not found'}), 404

@app.route('/admin/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = find_user_by_id(user_id)
    if user:
        users_db.remove(user)
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

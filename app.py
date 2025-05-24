from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock-Datenbanken
users_db = []
notes_db = []

# Hilfsfunktionen
def find_user_by_email(email):
    return next((user for user in users_db if user['email'] == email), None)

def find_user_by_id(user_id):
    return next((user for user in users_db if user['id'] == user_id), None)

def find_note_by_id(note_id):
    return next((note for note in notes_db if note['id'] == note_id), None)

# Endpunkte
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
    note_id = len(notes_db) + 1
    notes_db.append({
        'id': note_id,
        'title': data['title'],
        'content': data['content'],
        'owner_id': data['owner_id']
    })
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
    note = find_note_by_id(note_id)
    if note:
        note.update({
            'title': data['title'],
            'content': data['content']
        })
        return jsonify({'message': 'Note updated successfully'}), 200
    return jsonify({'error': 'Note not found'}), 404

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = find_note_by_id(note_id)
    if note:
        notes_db.remove(note)
        return jsonify({'message': 'Note deleted successfully'}), 200
    return jsonify({'error': 'Note not found'}), 404

@app.route('/admin/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = find_user_by_id(user_id)
    if user:
        users_db.remove(user)
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
        yield client

def test_register_success(client):
    response = client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'

def test_register_existing_user(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'User already exists'

def test_login_success(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'

def test_login_invalid_credentials(client):
    response = client.post('/login', json={
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid credentials'

def test_create_note_success(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/notes', json={
        'title': 'Test Note',
        'content': 'This is a test note.',
        'owner_id': 1
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Note created successfully'

def test_get_note_success(client):
    client.post('/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/notes', json={
        'title': 'Test Note',
        'content': 'This is a test note.',
        'owner_id': 1
    })
    response = client.get('/notes/1')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Note'

def test_get_note_not_found(client):
    response = client.get('/notes/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Note not found'

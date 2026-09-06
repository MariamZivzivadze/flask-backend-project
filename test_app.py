import os
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_signup_success(client):
    response = client.post('/api/signup', json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 201
    assert b"Welcome" in response.data

def test_signup_duplicate_email(client):
    client.post('/api/signup', json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    })
    response = client.post('/api/signup', json={
        "name": "Another User",
        "email": "test@example.com",
        "password": "anotherpass456"
    })
    assert response.status_code == 409

def test_login_success(client):
    client.post('/api/signup', json={
        "name": "Login User",
        "email": "login@example.com",
        "password": "correctpass"
    })
    response = client.post('/api/login', json={
        "email": "login@example.com",
        "password": "correctpass"
    })
    assert response.status_code == 200
    assert b"Welcome back" in response.data

def test_login_wrong_password(client):
    client.post('/api/signup', json={
        "name": "Login User",
        "email": "login2@example.com",
        "password": "correctpass"
    })
    response = client.post('/api/login', json={
        "email": "login2@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post('/api/login', json={
        "email": "doesnotexist@example.com",
        "password": "whatever"
    })
    assert response.status_code == 401
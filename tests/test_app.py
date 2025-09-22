import pytest
from app import create_app

def test_app_creation():
    """Test that app can be created successfully"""
    app = create_app('development')
    assert app is not None
    assert app.config['DEBUG'] is True

def test_security_headers(client):
    """Test that security headers are present"""
    response = client.get('/')
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert response.headers['X-Frame-Options'] == 'DENY'
    assert response.headers['X-XSS-Protection'] == '1; mode=block'

def test_home_page_loads(client):
    """Test that home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

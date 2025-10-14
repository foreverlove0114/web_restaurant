import pytest
from unittest.mock import patch
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"home" in response.data

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"about" in response.data

def test_contact_get(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b"contact" in response.data

@patch('routes.main_routes.requests.get')
@patch('routes.main_routes.logger')
def test_contact_post(mock_logger, mock_requests_get, client):
    form_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'subject': 'Hello',
        'message': 'This is a test message'
    }

    response = client.post('/contact', data=form_data)

    assert response.status_code == 200

    mock_requests_get.assert_called()
    called_url = mock_requests_get.call_args[0][0]
    assert "sendMessage" in called_url
    assert "Test User" in called_url
    assert "Hello" in called_url

    mock_logger.info.assert_called_with(
        'User with name Test User and email test@example.com sent a contact form.'
    )

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"login" in response.data

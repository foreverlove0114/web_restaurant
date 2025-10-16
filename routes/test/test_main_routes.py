from routes.test.conftest import BASE_URL
from routes.test.conftest import TEST_CONTACT_MESSAGE

def test_home_page(session):
    response = session.get(f"{BASE_URL}/")
    responseBody = response.text
    assert response.status_code == 200
    assert "Delicious dishes delivered straight to your home" in responseBody

def test_about_page(session):
    response = session.get(f"{BASE_URL}/about")
    assert response.status_code == 200
    assert "About Flask & Feats" in response.text

def test_getContact_page(session):
    response = session.get(f"{BASE_URL}/contact")
    assert response.status_code == 200
    assert "Send Us a Message" in response.text

def test_postContact_page(session):
    response = session.post(f"{BASE_URL}/contact",
                            data=TEST_CONTACT_MESSAGE)
    assert response.status_code == 200
    assert "We are always happy to hear from you" in response.text

import pytest

from routes.test.conftest import BASE_URL,extract_csrf_token


def test_user_profile_unauthenticated(session):
    response = session.get(f"{BASE_URL}/profile")
    assert response.status_code == 200
    assert "Account Login" in response.text

def test_user_profile_authenticated(logged_in_user):
    response = logged_in_user.get(f"{BASE_URL}/profile")
    assert response.status_code == 200
    assert "Personal information" in response.text
    assert "Manage your personal information and settings" in response.text
    assert "Your Profile" in response.text

def test_change_password(logged_in_user):
    get_response = logged_in_user.get(f"{BASE_URL}/profile")
    csrf_token = extract_csrf_token(get_response)

    post_data = {
        'oldpassword':'test123',
        'newpassword':'newtest123',
        'csrf_token':csrf_token
    }

    response = logged_in_user.post(f"{BASE_URL}/change-password", data=post_data)

    assert response.status_code == 200
    assert "Password changed successfully!" in response.text

    after_post_data = {
        'oldpassword': 'newtest123',
        'newpassword': 'test123',
        'csrf_token': csrf_token
    }

    logged_in_user.post(f"{BASE_URL}/change-password", data=after_post_data)

    print("密码更改测试成功，已将密码恢复")


def test_change_password_mismatch(logged_in_user):
    get_response = logged_in_user.get(f"{BASE_URL}/profile")
    csrf_token = extract_csrf_token(get_response)

    post_data = {
        'oldpassword': 'test1234',
        'newpassword': 'newtest123',
        'csrf_token': csrf_token
    }

    response = logged_in_user.post(f"{BASE_URL}/change-password", data=post_data)

    assert response.status_code == 200
    assert "Passwords do not match!" in response.text
    print("测试密码不match成功")


def test_change_address(logged_in_user):
    get_response = logged_in_user.get(f"{BASE_URL}/profile")
    csrf_token = extract_csrf_token(get_response)

    post_data = {
        'new_address':'456 street',
        'csrf_token': csrf_token
    }

    response = logged_in_user.post(f"{BASE_URL}/change-address", data=post_data)

    assert response.status_code == 200
    assert "Address updated successfully!" in response.text
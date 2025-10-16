#test_auth_routes.py
from routes.test.conftest import BASE_URL,TEST_USER,session,logged_in_user,extract_csrf_token

def test_register_get(session):
    response = session.get(f"{BASE_URL}/register")
    assert "Create Account" in response.text
    assert response.status_code == 200

def test_register_post_with_csrf(session):
    """带 CSRF token 的注册测试"""
    get_response = session.get(f"{BASE_URL}/register")
    csrf_token = extract_csrf_token(get_response)

    # 准备数据
    register_data = TEST_USER.copy()
    register_data['csrf_token'] = csrf_token

    # 提交注册
    response = session.post(f"{BASE_URL}/register", data=register_data)

    # 检查响应
    if response.status_code == 200:
        if "Delicious dishes" in response.text:
            print("✅ 注册成功并跳转到首页")
        elif "already exists" in response.text.lower():
            print("⚠️  用户已存在")
        else:
            print(f"📄 响应内容: {response.text[:300]}")
    else:
        print(f"❌ 注册失败，状态码: {response.status_code}")

    assert response.status_code == 200

def test_login_get(session):
    response = session.get(f"{BASE_URL}/login")
    assert response.status_code == 200
    assert "Glad to see you again!" in response.text

def test_login_post(session):
    get_response = session.get(f"{BASE_URL}/login")
    csrf_token = extract_csrf_token(get_response)

    login_data = {
        "nickname": TEST_USER["nickname"],
        "password": TEST_USER["password"],
        'csrf_token': csrf_token
    }

    response = session.post(f"{BASE_URL}/login",
                            data=login_data)

    assert response.status_code == 200
    if response.status_code == 200:
        if "Personal information" in response.text:
            print("✅ 登录成功并跳转到profile页面")
        elif "Incorrect nickname or password!" in response.text:
            print("登录失败")

def test_logout(logged_in_user):
    response = logged_in_user.get(f"{BASE_URL}/logout")
    assert response.status_code == 200
    assert "Login" in response.text
    assert "Register" in response.text

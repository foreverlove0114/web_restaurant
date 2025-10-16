from routes.test.conftest import (BASE_URL,
                                  random_product_id,
                                  extract_csrf_token,
                                  get_csrf_token_from_page)


def test_get_menu_page(session):
    response = session.get(f"{BASE_URL}/menu")
    assert response.status_code == 200
    assert "Our Menu" in response.text

def test_get_details(session,random_product_id):
    response = session.get(f"{BASE_URL}/position/{random_product_id}")
    assert response.status_code == 200
    assert "Ingredients:" in response.text
    assert "Description:" in response.text


def test_add_item_unauthenticated(session, random_product_id):
    """测试未登录用户尝试添加商品"""
    # 首先访问商品详情页面获取 CSRF token
    product_url = f"{BASE_URL}/position/{random_product_id}"
    csrf_token = get_csrf_token_from_page(session,product_url)

    # 准备 POST 数据（根据你的实际表单字段调整）
    add_item_data = {
        'csrf_token': csrf_token,
        'num': 1,  # 根据实际情况调整字段
    }

    # 发送 POST 请求添加商品
    response = session.post(product_url, data=add_item_data)

    # 断言
    assert response.status_code == 200
    assert "To add an item to the cart, please log in first!" in response.text
    print("✅ 未登录用户正确被阻止添加商品")

def test_add_item_authenticated(logged_in_user,random_product_id):
    product_url = f"{BASE_URL}/position/{random_product_id}"
    csrf_token = get_csrf_token_from_page(logged_in_user,product_url)

    add_item_data = {
        'csrf_token': csrf_token,
        'num':1
    }

    response = logged_in_user.post(product_url,data=add_item_data)

    assert response.status_code == 200
    assert "Item added to cart!" in response.text
    print("✅ 登录用户成功添加商品到购物车")


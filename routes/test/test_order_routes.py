from http.client import responses

import pytest
from bs4 import BeautifulSoup

from routes.test.conftest import BASE_URL, extract_csrf_token


def test_empty_order_page(session):
    """测试未登录用户访问空购物车页面"""
    """测试未登录用户页面中没有订单表单"""
    response = session.get(f"{BASE_URL}/create_order")
    soup = BeautifulSoup(response.text, 'html.parser')

    # 检查没有订单表单（因为购物车为空）
    checkout_form = soup.find('form', class_='checkout-form')
    assert checkout_form is None, "未登录用户不应该看到订单表单"

    assert response.status_code == 200
    assert "Your Cart is Empty" in response.text

    empty_basket = soup.find(class_='empty-basket')
    assert empty_basket is not None
    print("✅ 未登录用户页面正确显示空购物车，没有订单表单")

def test_cart_with_item(user_with_cart_item):
    """测试已登录用户有商品时创建订单"""
    response = user_with_cart_item.get(f"{BASE_URL}/create_order")
    assert response.status_code == 200
    assert "Selected Items" in response.text
    assert "Quantity: 1" in response.text
    assert "Total Price" in response.text


def test_create_order_post_with_items(user_with_cart_item):
    """测试有商品时提交订单"""
    # 先访问页面获取 CSRF token
    get_response = user_with_cart_item.get(f"{BASE_URL}/create_order")
    csrf_token = extract_csrf_token(get_response)

    post_data = {
        'csrf_token':csrf_token
    }

    response = user_with_cart_item.post(f"{BASE_URL}/create_order", data=post_data)

    assert response.status_code == 200
    assert "Items List:" in response.text
    assert "Date & Time" in response.text
    assert "Cancel Order" in response.text

def test_view_order_list(logged_in_user):
    response = logged_in_user.get(f"{BASE_URL}/my_orders")
    assert response.status_code == 200
    assert "Your Orders" in response.text
    assert "View Details" in response.text

def test_view_order_details(logged_in_user, created_order_id):
    order_id = created_order_id
    response = logged_in_user.get(f"{BASE_URL}/my_order/{order_id}")
    assert "Items List:" in response.text
    assert "Date & Time" in response.text
    assert "Cancel Order" in response.text


def test_cancel_order_successfully(user_with_place_order_already):
    """测试成功取消订单"""
    order_id = user_with_place_order_already.test_order_id

    response = user_with_place_order_already.post(f"{BASE_URL}/cancel_order/{order_id}")

    # 验证取消成功
    assert response.status_code == 200
    assert "Order deleted!" in response.text
    print(f"✅ 成功取消订单 {order_id}")

def test_cancel_order_non_exist_or_unauthorized(logged_in_user):
    """测试成功取消订单"""
    response = logged_in_user.post(f"{BASE_URL}/cancel_order/9999999")

    # 验证取消成功
    assert response.status_code == 200
    assert "Order not found or it is not yours!" in response.text

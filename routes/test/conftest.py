from http.client import responses

import pytest
import requests
import os
from bs4 import BeautifulSoup
import random
import re

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

TEST_USER = {
    "nickname": "testuser",
    "email": "testuser@email.com",
    "contact": "0123456789",
    "fullAddress": "123 street",
    "password": "test123"
}

TEST_CONTACT_MESSAGE = {
    "name": "testuser",
    "email": "testuser@gmail.com",
    "subject": "Complain about...",
    "message": "I wanna complain about..."
}

@pytest.fixture(scope="function")
def session():
    """创建 requests Session 保持会话状态"""
    return requests.Session()

@pytest.fixture(scope="function")
def logged_in_user(session):
    get_response = session.get(f"{BASE_URL}/login")
    csrf_token = extract_csrf_token(get_response)

    login_data = {
        "nickname": TEST_USER["nickname"],
        "password": TEST_USER["password"],
        'csrf_token': csrf_token
    }

    session.post(f"{BASE_URL}/login", data=login_data)
    return session

@pytest.fixture(scope="function")
def random_product_id(session):
    """返回一个随机的产品 ID"""
    product_ids = get_all_product_ids(session)

    if not product_ids:
        # 如果没有找到产品 ID，使用默认的备选列表
        default_ids = [2, 3, 4, 5, 6, 7, 9]
        product_id = random.choice(default_ids)
        print(f"⚠️  使用默认产品 ID: {product_id}")
    else:
        product_id = random.choice(product_ids)
        print(f"✅ 随机选择产品 ID: {product_id}")

    return product_id

@pytest.fixture(scope="function")
def user_with_cart_item(logged_in_user, random_product_id):
    product_url = f"{BASE_URL}/position/{random_product_id}"
    csrf_token = get_csrf_token_from_page(logged_in_user, product_url)

    add_item_data = {
        'csrf_token': csrf_token,
        'num': 1
    }

    logged_in_user.post(product_url, data=add_item_data)
    return logged_in_user


@pytest.fixture(scope="function")
def user_with_place_order_already(user_with_cart_item):
    """创建订单并返回包含订单ID的session"""
    get_response = user_with_cart_item.get(f"{BASE_URL}/create_order")
    csrf_token = extract_csrf_token(get_response)

    post_data = {'csrf_token': csrf_token}
    response = user_with_cart_item.post(f"{BASE_URL}/create_order", data=post_data)

    # 从响应文本中提取订单ID
    order_id = extract_order_id_from_text(response.text)

    if order_id:
        user_with_cart_item.test_order_id = order_id
        print(f"✅ 从响应文本提取订单ID: {order_id}")
        return user_with_cart_item
    pytest.skip("无法从响应中提取订单ID")
    return None


def extract_csrf_token(html_content):
    """从 HTML 中提取 CSRF token"""
    if hasattr(html_content, 'text'):
        html_content = html_content.text
    soup = BeautifulSoup(html_content, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    return csrf_input.get('value') if csrf_input else None

def get_csrf_token_from_page(session, url):
    """从指定页面提取 CSRF token"""
    response = session.get(url)
    return extract_csrf_token(response)

def get_all_product_ids(session):
    """从菜单页面获取所有产品 ID"""
    try:
        response = session.get(f"{BASE_URL}/menu")
        response.raise_for_status() # 如果状态码不是200，抛出异常

        soup = BeautifulSoup(response.text, 'html.parser')
        product_links = soup.find_all('a', href=True, class_='btn')

        product_ids = []
        for link in product_links:
            href = link['href']
            if href.startswith('/position/'):
                product_id = href.split('/')[-1]  # 从 "/position/9" 中提取 "9"
                if product_id.isdigit():
                    product_ids.append(int(product_id))

        return product_ids
    except Exception as e:
        print(f"获取产品 ID 失败: {e}")
        return []

def extract_order_id_from_text(text):
    """从文本中提取订单ID"""
    # 方法1: 匹配 "Your Order №5" 格式
    pattern1 = r'Your Order №(\d+)'
    match1 = re.search(pattern1, text)
    if match1:
        return int(match1.group(1))
    return None



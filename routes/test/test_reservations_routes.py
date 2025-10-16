import pytest
import requests

from routes.test.conftest import BASE_URL,extract_csrf_token
from datetime import datetime, timedelta

def get_future_time(days=1):
    """生成未来时间"""
    return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%dT%H:%M')

def test_get_reserved_page_unauthenticated(session):
    response = session.get(f"{BASE_URL}/reserved")
    assert response.status_code == 200
    assert "Please log in to access this page." in response.text

def test_get_reserved_page_authenticated(logged_in_user):
    response = logged_in_user.get(f"{BASE_URL}/reserved")
    assert response.status_code == 200
    assert "Table Reservation" in response.text
    assert "Table Type:" in response.text
    assert "Reservation Time:" in response.text
    assert "Make Reservation" in response.text

def test_reserved_more_than_one(logged_in_user):
    pass


def test_reserved_clash_with_time_same_user(logged_in_user):
    pass


def test_reserved_different_scenarios(logged_in_user):
    """测试成功创建预约"""
    get_response = logged_in_user.get(f"{BASE_URL}/reserved")
    csrf_token = extract_csrf_token(get_response)

    post_data = {
        'table_type': "2",
        'time': get_future_time(),
        'csrf_token': csrf_token
    }

    response = logged_in_user.post(f"{BASE_URL}/reserved", data=post_data)

    assert response.status_code == 200
    if "for a 2-person table successfully created!" in response.text:
        print("你已经预约成功了！")
    elif "You can have only one active reservation." in response.text:
        print("你只能有一次的预约！")
    elif "Unfortunately, a reservation for this type of table is currently not available" in response.text:
        print("该时段的桌位已经被预约了！")


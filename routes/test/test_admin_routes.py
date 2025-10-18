from http.client import responses

import pytest
from PIL import Image
import io
from online_restaurant_db import Session,Menu
from fill_menu import download_image
from routes.test.conftest import BASE_URL,extract_csrf_token


def test_get_add_position(logged_in_admin):
    response = logged_in_admin.get(f"{BASE_URL}/add_position")
    assert response.status_code == 200
    assert "Adding a new item" in response.text
    assert "Add product" in response.text


def test_get_add_position_user(logged_in_user):
    response = logged_in_user.get(f"{BASE_URL}/add_position")
    assert response.status_code == 200
    assert "Access denied! Only administrators can add new items" in response.text

def test_post_add_position(logged_in_admin):
    get_response = logged_in_admin.get(f"{BASE_URL}/add_position")
    csrf_token = extract_csrf_token(get_response)

    # 创建模拟图片文件
    image_file = create_test_image_red()

    add_position = {
        'name':'Test Pizza',
        'ingredients': 'Cheese, Tomato, Dough',
        'description': 'A delicious test pizza',
        'price': '25',
        'weight': '300',
        'csrf_token': csrf_token
    }

    files = {
        'img': ('test_pizza.jpg', image_file, 'image/jpeg')
    }

    # 提交表单
    response = logged_in_admin.post(
        f"{BASE_URL}/add_position",
        data=add_position,
        files=files
    )

    assert response.status_code == 200
    assert "Item added successfully!" in response.text
    print("✅ 管理员成功添加菜品")

def test_post_add_position_NoImage(logged_in_admin):
    get_response = logged_in_admin.get(f"{BASE_URL}/add_position")
    csrf_token = extract_csrf_token(get_response)

    # 创建模拟图片文件
    # image_file = create_test_image()

    add_position = {
        'name': 'Test Pizza',
        'ingredients': 'Cheese, Tomato, Dough',
        'description': 'A delicious test pizza',
        'price': '25',
        'weight': '300',
        'csrf_token': csrf_token
    }

    # files = {
    #     'img': ('test_pizza.jpg', image_file, 'image/jpeg')
    # }

    # 提交表单
    response = logged_in_admin.post(
        f"{BASE_URL}/add_position",
        data=add_position
    )

    assert response.status_code == 200
    assert "No file selected or upload failed" in response.text
    print("✅ 成功检测到缺少文件")

def test_get_edit_position(logged_in_admin):
    response = logged_in_admin.get(f"{BASE_URL}/edit_position/2")
    assert response.status_code == 200
    assert "Editing item" in response.text
    assert "Active" in response.text

def test_get_edit_position_user(logged_in_user):
    response = logged_in_user.get(f"{BASE_URL}/edit_position/2")
    assert response.status_code == 200
    assert "Access denied! Only administrators can edit menu." in response.text

def test_post_edit_position(logged_in_admin):
    """基础编辑菜品测试"""
    # 获取编辑页面
    get_response = logged_in_admin.get(f"{BASE_URL}/edit_position/2")
    csrf_token = extract_csrf_token(get_response)

    # 准备编辑数据
    edit_data = {
        'csrf_token': csrf_token,
        "name": "Margherita",
        "weight": "430",
        "ingredients": "Dough, tomato sauce, mozzarella, basil, olive oil",
        "description": "Classic Italian pizza with delicate tomato sauce, fresh mozzarella and aromatic basil. Perfect choice for lovers of traditional Italian cuisine.",
        "price": 190
    }

    # 提交编辑
    response = logged_in_admin.post(
        f"{BASE_URL}/edit_position/2",
        data=edit_data
    )

    assert response.status_code == 200
    assert "Position successfully edited!" in response.text
    assert "Our Menu" in response.text

def test_post_edit_position_image(logged_in_admin):
    get_response = logged_in_admin.get(f"{BASE_URL}/edit_position/10")
    csrf_token = extract_csrf_token(get_response)

    new_image = create_test_image_blue()

    # 准备编辑数据
    edit_data = {
        'csrf_token': csrf_token,
        "name": "Margherita",
        "weight": "450",
        "ingredients": "Dough, tomato sauce, mozzarella, basil, olive oil",
        "description": "Classic Italian pizza with delicate tomato sauce, fresh mozzarella and aromatic basil. Perfect choice for lovers of traditional Italian cuisine.",
        "price": 180
    }

    files = {
        'img': ('new_image.jpg', new_image, 'image/jpeg')
    }

    response = logged_in_admin.post(f"{BASE_URL}/edit_position/10",
                                    data=edit_data,
                                    files = files)

    assert response.status_code == 200
    assert "Position successfully edited!" in response.text
    assert "Our Menu" in response.text

def test_user_check_reservation(logged_in_user):
    response = logged_in_user.get(f"{BASE_URL}/reservations_check")
    assert response.status_code == 200
    assert "Access denied! Only administrators can check reservations" in response.text

def test_admin_check_reservation(logged_in_admin):
    response = logged_in_admin.get(f"{BASE_URL}/reservations_check")
    assert response.status_code == 200
    assert "Checking reservations" in response.text

def test_admin_delete_reservation(logged_in_admin,get_first_reservation_id):
    get_response = logged_in_admin.get(f"{BASE_URL}/reservations_check")
    csrf_token = extract_csrf_token(get_response)
    reservation_id = get_first_reservation_id

    if not reservation_id:
        pytest.skip("没有找到可删除的预订记录")

    post_delete_reservation = {
        'reserv_id':reservation_id,
        'csrf_token':csrf_token
    }

    response = logged_in_admin.post(f"{BASE_URL}/reservations_check",data=post_delete_reservation)

    assert response.status_code == 200
    print(f"✅ 成功删除预订 ID: {reservation_id}")

def test_user_check_menu(logged_in_user):
    response = logged_in_user.get(f"{BASE_URL}/menu_check")
    assert response.status_code == 200
    assert "Access denied! Only administrators can check menu" in response.text

def test_admin_check_menu(logged_in_admin):
    response = logged_in_admin.get(f"{BASE_URL}/menu_check")
    assert response.status_code == 200
    assert "Перевірка меню" in response.text

def test_menu_check_change_status(logged_in_admin):
    get_response = logged_in_admin.get(f"{BASE_URL}/menu_check")
    csrf_token = extract_csrf_token(get_response)

    # 准备改变状态的数据
    post_change_status = {
        'csrf_token':csrf_token,
        'pos_id':10,
        'change_status':''
    }

    response = logged_in_admin.post(
        f"{BASE_URL}/menu_check",
        data=post_change_status
    )

    assert response.status_code == 200
    # 检查页面是否重新加载了菜单列表
    assert "Ні" or "Так" in response.text
    print("✅ 成功改变菜品状态")

def test_menu_check_delete_position(logged_in_admin):
    get_response = logged_in_admin.get(f"{BASE_URL}/menu_check")
    csrf_token = extract_csrf_token(get_response)

    # 准备改变状态的数据
    post_change_status = {
        'csrf_token':csrf_token,
        'pos_id':10,
        'delete_position':''
    }

    response = logged_in_admin.post(
        f"{BASE_URL}/menu_check",
        data=post_change_status
    )

    assert response.status_code == 200
    # 检查页面是否重新加载了菜单列表
    assert "Test Pizza" not in response.text
    print("✅ 成功删除测试菜品")

def test_admin_get_all_users(logged_in_admin):
    response = logged_in_admin.get(f"{BASE_URL}/all_users")
    assert response.status_code == 200
    assert "Users" in response.text

######################################################################
#                       辅助方法
######################################################################
def create_test_image_red():
    """创建测试图片文件"""
    # 创建一个简单的1x1像素图片
    image = Image.new('RGB', (1, 1), color='red')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_test_image_blue():
    """创建测试图片文件"""
    # 创建一个简单的1x1像素图片
    image = Image.new('RGB', (1, 1), color='blue')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr



# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from routes.menu_routes import position

import sys
import os
import pytest

# 关键修复：添加正确的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 添加两条路径确保覆盖所有情况
sys.path.insert(0, current_dir)    # end_to_end 目录
sys.path.insert(0, parent_dir)     # 项目根目录

print(f"🔧 conftest.py 调试信息:")
print(f"   当前文件: {__file__}")
print(f"   当前目录: {current_dir}")
print(f"   父目录: {parent_dir}")
print(f"   Python路径: {sys.path}")

# 现在导入页面模块
try:
    from Pages.HomePage import HomePage
    from Pages.LoginPage import LoginPage
    from Pages.ProfilePage import ProfilePage
    print("✅ 成功导入所有页面模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    # 详细调试
    pages_dir = os.path.join(current_dir, 'Pages')
    print(f"📁 Pages目录: {pages_dir}")
    print(f"📁 Pages目录存在: {os.path.exists(pages_dir)}")
    if os.path.exists(pages_dir):
        print(f"📁 Pages目录内容: {os.listdir(pages_dir)}")
    raise


@pytest.fixture(scope="function")
def browser():
    """创建浏览器实例"""
    options = webdriver.ChromeOptions()

    # Disable the data breach alerts (password leak detection)
    options.add_experimental_option(
        "prefs", {"profile.password_manager_leak_detection": False}
    )

    # Other useful options for automation (optional, but recommended)
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option("excludeSwitches",
                                           ["enable-automation"])  # Hides the "Chrome is being controlled..." message

    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    # 设置基础URL
    driver.get("http://localhost:8000/")

    print(f"把driver交给Home Page")
    yield driver



    # teardown
    print(f"退出driver")
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_profile_page(browser):
    """已登录用户夹具"""
    from Pages.HomePage import HomePage
    from Pages.LoginPage import LoginPage

    home_page = HomePage(browser)

    # 如果未登录，则先登录
    if home_page.is_user_logged_out():
        print(f"开始用户登录流程")

        # 导航到登录页面并执行登录
        login_page = home_page.navigate_to_login()
        profile_page = login_page.login("testuser", "test123")

        # 验证登录成功
        assert profile_page.get_page_title() == "Your Profile", "登录后未正确跳转到个人资料页"
        print("✅ 用户登录成功并跳转到个人资料页")

        return profile_page  # ✅ 返回 ProfilePage

    else:
        # 用户已登录，导航到个人资料页
        print("ℹ️ 用户已登录，导航到个人资料页")
        profile_page = home_page.navigate_to_profile()
        return profile_page

@pytest.fixture(scope="function")
def order_page_with_item(logged_in_profile_page):

    menu_page = logged_in_profile_page.navigate_to_menu()

    position_page = menu_page.view_item_details(0)
    position_page.add_to_cart(2)

    order_page = position_page.navigate_to_cart()

    return order_page

# @pytest.fixture(scope="function")
# def admin_user(browser):
#     """管理员用户夹具"""
#     from Pages.HomePage import HomePage
#     from Pages.LoginPage import LoginPage
#
#     home_page = HomePage(browser)
#
#     # 如果未登录，则使用管理员账号登录
#     if home_page.is_user_logged_out():
#         login_page = home_page.navigate_to_login()
#         login_page.login("admin", "adminpassword")
#
#     return home_page
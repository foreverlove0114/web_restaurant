# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def browser():
    """创建浏览器实例"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
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
def logged_in_user(browser):
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
# tests/test_cases/test_navigation.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v140.page import navigate
import time


class TestNavigation:
    """导航功能测试用例"""

    def test_home_page_loaded_successfully(self, browser):
        print(f"🚀 测试开始，browser ID: {id(browser)}")

        from Pages.HomePage import HomePage
        home_page = HomePage(browser)
        print(f"📄 HomePage 实例创建完成，home_page.driver ID: {id(home_page.driver)}")

        result = home_page.is_hero_section_visible()
        print(f"✅ 断言结果: {result}")

        assert result, "首页英雄区域未显示"

    def test_navbar_links_present(self, browser):
        """测试导航栏链接存在"""
        from Pages.HomePage import HomePage
        home_page = HomePage(browser)

        navbar_links = home_page.get_navbar_links()
        expected_links = ["Home", "Menu", "Reservations", "About Us", "Contact"]

        assert navbar_links == expected_links, f"导航栏链接不匹配: {navbar_links}"

    def test_navigate_to_about_page(self, browser):
        """测试导航到关于我们页面"""
        from Pages.HomePage import HomePage
        from Pages.AboutPage import AboutPage

        home_page = HomePage(browser)
        about_page = home_page.navigate_to_about()

        assert about_page.get_page_title() == "About Flask & Feats", "关于我们页面标题不正确"
        assert about_page.is_our_story_section_visible(), "Our Story部分未显示"
        assert about_page.is_our_values_section_visible(), "Our Values部分未显示"
        assert about_page.is_our_team_section_visible(), "Our Team部分未显示"

    def test_navigate_to_contact_page(self, browser):
        """测试导航到联系页面"""
        from Pages.HomePage import HomePage
        from Pages.ContactPage import ContactPage

        home_page = HomePage(browser)
        contact_page = home_page.navigate_to_contact()

        assert contact_page.get_page_title() == "Contact Us", "联系页面标题不正确"
        assert contact_page.is_contact_form_present(), "联系表单未显示"
        assert contact_page.get_info_cards_count() == 4, "信息卡片数量不正确"

    def test_navigate_to_menu_page(self, browser):
        """测试导航到菜单页面"""
        from Pages.HomePage import HomePage
        from Pages.MenuPage import MenuPage

        home_page = HomePage(browser)
        menu_page = home_page.navigate_to_menu()

        assert menu_page.get_page_title() == "Our Menu", "菜单页面标题不正确"
        assert menu_page.is_element_present(MenuPage.SEARCH_INPUT), "搜索框未显示"

    def test_view_menu_button_redirects_to_menu(self, browser):
        """测试查看菜单按钮重定向到菜单页面"""
        from Pages.HomePage import HomePage
        from Pages.MenuPage import MenuPage

        home_page = HomePage(browser)
        menu_page = home_page.click_view_menu()

        assert menu_page.get_page_title() == "Our Menu", "查看菜单按钮未正确重定向"


# tests/test_cases/test_authentication.py
import pytest


class TestAuthentication:
    """用户认证测试用例"""

    def test_navigate_to_login_page(self, browser):
        """测试导航到登录页面"""
        from Pages.HomePage import HomePage
        from Pages.LoginPage import LoginPage

        home_page = HomePage(browser)
        login_page = home_page.navigate_to_login()

        assert login_page.is_login_form_present(), "登录表单未显示"
        assert login_page.is_element_present(LoginPage.NICKNAME_INPUT), "用户名输入框未显示"
        assert login_page.is_element_present(LoginPage.PASSWORD_INPUT), "密码输入框未显示"

    def test_navigate_to_register_page(self, browser):
        """测试导航到注册页面"""
        from Pages.HomePage import HomePage
        from Pages.RegisterPage import RegisterPage

        home_page = HomePage(browser)
        register_page = home_page.navigate_to_register()

        assert register_page.is_element_present(RegisterPage.NICKNAME_INPUT), "用户名输入框未显示"
        assert register_page.is_element_present(RegisterPage.EMAIL_INPUT), "邮箱输入框未显示"
        assert register_page.is_element_present(RegisterPage.CONTACT_INPUT), "联系电话输入框未显示"
        assert register_page.is_element_present(RegisterPage.ADDRESS_INPUT), "地址输入框未显示"
        assert register_page.is_element_present(RegisterPage.PASSWORD_INPUT), "密码输入框未显示"

    def test_successful_login(self, browser):
        """测试成功登录"""
        from Pages.HomePage import HomePage
        from Pages.ProfilePage import ProfilePage

        home_page = HomePage(browser)
        login_page = home_page.navigate_to_login()

        # 使用测试账号登录
        profile_page = login_page.login("testuser", "test123")

        # 验证登录成功
        assert profile_page.get_page_title() == "Your Profile", "未正确跳转至Profile Page"
        assert profile_page.is_element_present(ProfilePage.USER_INFO), "未正确展示用户信息"
        assert profile_page.is_element_present(ProfilePage.OLD_PASSWORD_INPUT), "未正确展示更改密码输入位"

    def test_failed_login_invalid_credentials(self, browser):
        """测试使用无效凭据登录失败"""
        from Pages.HomePage import HomePage
        from Pages.LoginPage import LoginPage

        home_page = HomePage(browser)
        login_page = home_page.navigate_to_login()

        # 使用无效凭据登录
        login_page.login("invalid_user", "wrong_password")

        # 验证登录失败
        flash_message = login_page.get_flash_message()
        assert flash_message is not None, "未显示错误消息"
        assert flash_message == "Incorrect nickname or password!", "未正确显示错误信息"

    def test_user_registration(self, browser):
        """测试用户注册"""
        from Pages.HomePage import HomePage
        from Pages.RegisterPage import RegisterPage
        import random

        home_page = HomePage(browser)
        register_page = home_page.navigate_to_register()

        # 生成随机用户名避免重复
        random_username = f"testuser_{random.randint(1000, 9999)}"

        # 填写注册表单
        current_home_page = register_page.register(
            nickname=random_username,
            email=f"{random_username}@test.com",
            contact="+380123456789",
            address="Test City, Test Street, 123",
            password="testpassword123"
        )

        # 验证注册结果
        assert current_home_page.is_hero_section_visible() is not None, "未显示注册结果消息"
        assert current_home_page.is_element_present(HomePage.PROFILE_LINK),"没有成功注册后直接登录"

    def test_logout_functionality(self, logged_in_profile_page):
        """测试退出登录功能"""
        from Pages.HomePage import HomePage

        home_page = logged_in_profile_page
        home_page.click_logout()

        # 验证退出成功
        assert home_page.is_user_logged_out(), "用户退出登录状态不正确"
        # assert home_page.is_element_present(HomePage.LOGIN_LINK), "登录链接未显示"

class TestMenu:

    def test_menu_page_loaded_successfully(self,browser):
        from Pages.HomePage import HomePage
        from Pages.MenuPage import MenuPage

        home_page = HomePage(browser)
        menu_page = home_page.navigate_to_menu()
        print(f"成功导航至menu page")

        assert menu_page.get_page_title() == "Our Menu", "菜单页面标题不正确"
        assert menu_page.is_element_present(MenuPage.SEARCH_INPUT), "搜索框未显示"
        assert menu_page.is_element_present(MenuPage.SEARCH_BUTTON), "搜索按钮未显示"

    def test_menu_items_displayed(self,browser):
        from Pages.HomePage import HomePage

        home_page = HomePage(browser)
        menu_page = home_page.navigate_to_menu()

        item_count = menu_page.get_menu_items_count()
        assert item_count >=0, "菜单项数量异常"

        # 如果有菜单项，检查第一个菜单项的信息
        if item_count > 0:
            first_item = menu_page.get_menu_item_info(0)
            assert first_item is not None, "无法获取菜单项信息"
            assert "name" in first_item and first_item["name"], "菜单项名称为空"
            assert "price" in first_item and first_item["price"], "菜单项价格为空"

    def test_menu_search_functionality(self, browser):
        from Pages.HomePage import HomePage

        home_page = HomePage(browser)
        menu_page = home_page.navigate_to_menu()

        # 添加调试信息
        initial_count = menu_page.get_menu_items_count()
        print(f"搜索前菜单项数量: {initial_count}")

        menu_page.search_menu_items("Margherita")

        # 添加等待，确保搜索完成
        import time
        time.sleep(2)

        after_search_count = menu_page.get_menu_items_count()
        print(f"搜索后菜单项数量: {after_search_count}")
        print(f"搜索关键词: Margherita")

        # 先检查搜索是否有效
        if after_search_count == initial_count:
            print("⚠️ 搜索可能没有生效")
        elif after_search_count >= 1:
            print(f"🔍 搜索返回了 {after_search_count} 个结果")

        # 修改断言，先验证搜索功能是否工作
        assert after_search_count < initial_count, "搜索功能未生效"
        assert after_search_count == 1, "搜索结果为空"


    def test_view_menu_item_details(self,browser):
        from Pages.HomePage import HomePage

        home_page = HomePage(browser)
        menu_page = home_page.navigate_to_menu()

        # 只有在有菜单项时才执行详情测试
        if menu_page.get_menu_items_count() > 0:
            position_page = menu_page.view_item_details(0)

            assert position_page is not None, "无法打开商品详情页面"
            assert position_page.get_position_title() != "", "商品标题为空"
            assert position_page.get_price() != "", "商品价格为空"
            assert position_page.is_image_visible(), "商品图片未显示"

    def test_menu_items_details_content(self,browser):
        from Pages.HomePage import HomePage

        home_page = HomePage(browser)
        menu_page = home_page.navigate_to_menu()

        if menu_page.get_menu_items_count() > 0:
            position_page = menu_page.view_item_details(0)

            # 验证详情页面内容
            ingredients = position_page.get_ingredients()
            description = position_page.get_description()

            assert ingredients != "", "商品成分为空"
            assert description != "", "商品描述为空"

class TestOrders:
    """订单功能测试用例"""

    def test_empty_cart_display(self,logged_in_profile_page):
        from Pages.OrderPage import OrderPage

        order_page = logged_in_profile_page.navigate_to_cart()

        if order_page.is_basket_empty():
            assert "Your Cart is Empty" in order_page.get_text(OrderPage.EMPTY_BASKET_MESSAGE), "空购物车消息不正确"

    def test_add_item_to_cart(self,logged_in_profile_page):
        """测试添加商品到购物车"""
        from Pages.PositionPage import PositionPage

        menu_page = logged_in_profile_page.navigate_to_menu()

        if menu_page.get_menu_items_count() > 0:
            position_page = menu_page.view_item_details(0)
            print(f"Your are in the page of {position_page.get_text(PositionPage.POSITION_TITLE)}")
            position_page.add_to_cart(2)

            assert "Item added to cart!" in position_page.flash_message_to_add_item()
            print(f"{position_page.flash_message_to_add_item()}")

    def test_cart_total_price_calculation(self, order_page_with_item):
        assert "380 UAH" in order_page_with_item.get_total_price(), "未显示正确金额"
        print(f"Price as: {order_page_with_item.get_total_price()}")

    def test_place_order_functionality(self,order_page_with_item):
        """测试下订单功能"""
        my_order = order_page_with_item.place_order()

        assert "Your Order" in my_order.get_order_title(), "未正确显示my order"
        assert "380 UAH" in my_order.get_total_price(), "未显示正确金额"
        assert my_order.is_cancel_button_present(), "未正确显示取消按钮"

    def test_navigate_to_active_orders(self,order_page_with_item):

        my_orders = order_page_with_item.navigate_to_active_orders()

        assert my_orders.get_page_title() == "Your Orders", "未正确跳转到我的订单页面"
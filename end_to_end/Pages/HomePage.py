# tests/pages/home_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class HomePage(BasePage):
    # 导航栏定位器
    NAVBAR_HOME = (By.LINK_TEXT, "Home")
    NAVBAR_MENU = (By.LINK_TEXT, "Menu")
    NAVBAR_RESERVATIONS = (By.LINK_TEXT, "Reservations")
    NAVBAR_ABOUT = (By.LINK_TEXT, "About Us")
    NAVBAR_CONTACT = (By.LINK_TEXT, "Contact")

    # 认证链接定位器
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    PROFILE_LINK = (By.LINK_TEXT, "Profile")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")

    # 首页内容定位器
    HERO_SECTION = (By.CLASS_NAME, "hero-section")
    CTA_BUTTON = (By.LINK_TEXT, "View Menu")
    FEATURE_CARDS = (By.CLASS_NAME, "feature-card")
    CART_ICON = (By.CLASS_NAME, "cart-icon")

    def __init__(self, driver):
        print(f"🔧 HomePage 初始化，接收到 driver: {id(driver)}")
        super().__init__(driver)
        self.driver = driver
        print(f"🔧 HomePage 初始化完成，self.driver: {id(self.driver)}")

    def navigate_to_menu(self):
        print(f"开始导航至menu page")
        self.click_element(self.NAVBAR_MENU)
        from .MenuPage import MenuPage
        return MenuPage(self.driver)

    # def navigate_to_reservations(self):
    #     """导航到预订页面"""
    #     self.click_element(self.NAVBAR_RESERVATIONS)
    #     from .ReservationsPage import ReservationsPage
    #     return ReservationsPage(self.driver)

    def navigate_to_about(self):
        """导航到关于我们页面"""
        self.click_element(self.NAVBAR_ABOUT)
        from .AboutPage import AboutPage
        return AboutPage(self.driver)

    def navigate_to_contact(self):
        """导航到联系页面"""
        self.click_element(self.NAVBAR_CONTACT)
        from .ContactPage import ContactPage
        return ContactPage(self.driver)

    def navigate_to_login(self):
        """导航到登录页面"""
        self.click_element(self.LOGIN_LINK)
        from .LoginPage import LoginPage
        print(f"进入登录页面")
        return LoginPage(self.driver)

    def navigate_to_register(self):
        """导航到注册页面"""
        self.click_element(self.REGISTER_LINK)
        from .RegisterPage import RegisterPage
        return RegisterPage(self.driver)

    def navigate_to_profile(self):
        """导航到个人资料页面"""
        self.click_element(self.PROFILE_LINK)
        from .ProfilePage import ProfilePage
        return ProfilePage(self.driver)

    def click_logout(self):
        self.click_element(self.LOGOUT_LINK)

    def click_view_menu(self):
        self.click_element(self.CTA_BUTTON)
        from .MenuPage import MenuPage
        return MenuPage(self.driver)

    def is_user_logged_in(self):
        return self.is_element_present(self.PROFILE_LINK)

    def is_user_logged_out(self):
        return self.is_element_present(self.LOGIN_LINK)

    def get_feature_cards_count(self):
        return len(self.find_elements(self.FEATURE_CARDS))

    def is_hero_section_visible(self):
        print(f"🔍 正在检查英雄区域，使用 driver: {id(self.driver)}")
        return self.is_element_present(self.HERO_SECTION)

    def get_navbar_links(self):
        links = self.find_elements((By.CSS_SELECTOR, ".nav-links a"))
        return [link.text for link in links]
# tests/pages/login_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class LoginPage(BasePage):
    # 表单元素定位器
    NICKNAME_INPUT = (By.ID, "nickname")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CLASS_NAME, "btn-auth")

    # 导航链接定位器
    REGISTER_LINK = (By.LINK_TEXT, "Register")

    # 消息定位器
    FLASH_MESSAGES = (By.CLASS_NAME, "alert")

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    def login(self,nickname,password):
        self.send_keys(self.NICKNAME_INPUT,nickname)
        self.send_keys(self.PASSWORD_INPUT,password)
        self.click_element(self.LOGIN_BUTTON)

    def get_flash_message(self):
        if self.is_element_present(self.FLASH_MESSAGES):
           return self.get_text(self.FLASH_MESSAGES)
        return None

    def navigate_to_register(self):
        """导航到注册页面"""
        self.click_element(self.REGISTER_LINK)
        from .RegisterPage import RegisterPage
        return RegisterPage(self.driver)

    def is_login_form_present(self):
        """检查登录表单是否存在"""
        return (self.is_element_present(self.NICKNAME_INPUT) and
                self.is_element_present(self.PASSWORD_INPUT))

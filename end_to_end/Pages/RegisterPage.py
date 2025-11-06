# tests/pages/register_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class RegisterPage(BasePage):
    # 表单元素定位器
    NICKNAME_INPUT = (By.ID, "nickname")
    EMAIL_INPUT = (By.ID, "email")
    CONTACT_INPUT = (By.ID, "contact")
    ADDRESS_INPUT = (By.ID, "fullAddress")
    PASSWORD_INPUT = (By.ID, "password")
    REGISTER_BUTTON = (By.CLASS_NAME, "btn-auth")

    # 导航链接定位器
    LOGIN_LINK = (By.LINK_TEXT, "Log in")

    # 消息定位器
    FLASH_MESSAGES = (By.CLASS_NAME, "alert")

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    def register(self,nickname,email,contact,address,password):
        self.send_keys(self.NICKNAME_INPUT,nickname)
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.CONTACT_INPUT, contact)
        self.send_keys(self.ADDRESS_INPUT, address)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click_element(self.REGISTER_BUTTON)

    # def get_flash_message(self):
    #     if self.is_element_present(self.FLASH_MESSAGES):
    #         return self.get_text(self.FLASH_MESSAGES)
    #     return None

    def navigate_to_login(self):
        self.click_element(self.LOGIN_LINK)
        from .LoginPage import LoginPage
        return LoginPage(self.driver)
# tests/pages/profile_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class ProfilePage(BasePage):
    # 管理员功能定位器
    # ADMIN_LINKS = (By.CSS_SELECTOR, ".admin-content a")

    # 个人信息定位器
    USER_INFO = (By.CLASS_NAME, "info-value")

    # 修改密码定位器
    OLD_PASSWORD_INPUT = (By.ID, "oldpassword")
    NEW_PASSWORD_INPUT = (By.ID, "newpassword")
    CHANGE_PASSWORD_BUTTON = (By.XPATH, "//button[contains(text(), 'Change password')]")

    # 修改地址定位器
    NEW_ADDRESS_INPUT = (By.ID, "new_address")
    CHANGE_ADDRESS_BUTTON = (By.XPATH, "//button[contains(text(), 'Change address')]")

    # 退出登录定位器
    LOGOUT_BUTTON = (By.CLASS_NAME, "btn-logout")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_user_info(self):
        info_elements = self.find_elements(self.USER_INFO)
        return{
            'nickname':info_elements[0].text if len(info_elements) > 0 else '',
            'email':info_elements[1].text if len(info_elements) > 1 else '',
            'phone':info_elements[2].text if len(info_elements) > 2 else '',
            'address':info_elements[3].text if len(info_elements) > 3 else ''
        }

    def change_password(self,old_password,new_password):
        self.send_keys(self.OLD_PASSWORD_INPUT,old_password)
        self.send_keys(self.NEW_PASSWORD_INPUT,new_password)
        self.click_element(self.CHANGE_PASSWORD_BUTTON)

    def change_address(self,new_address):
        self.send_keys(self.NEW_ADDRESS_INPUT,new_address)
        self.click_element(self.CHANGE_PASSWORD_BUTTON)

    def logout(self):
        self.click_element(self.LOGOUT_BUTTON)
        from .HomePage import HomePage
        return HomePage(self.driver)

    # def get_admin_links(self):
    #     if self.is_element_present(self.ADMIN_LINKS):
    #         links = self.find_elements(self.ADMIN_LINKS)
    #         return [link.text for link in links]
    #     return []


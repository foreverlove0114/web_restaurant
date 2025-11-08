# tests/pages/contact_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage


class ContactPage(BasePage):
    """
    联系页面对象
    封装联系页面的所有元素定位和操作
    """

    # 页面元素定位器
    PAGE_TITLE = (By.CLASS_NAME, "page-title")
    CONTACT_FORM = (By.CLASS_NAME, "contact-form")
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    SUBJECT_INPUT = (By.ID, "subject")
    MESSAGE_INPUT = (By.ID, "message")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Send Message')]")
    INFO_CARDS = (By.CLASS_NAME, "info-card")
    MAP_CONTAINER = (By.CLASS_NAME, "map-container")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_page_title(self):
        """获取页面标题"""
        return self.get_text(self.PAGE_TITLE)

    def is_contact_form_present(self):
        """检查联系表单是否存在"""
        return self.is_element_present(self.CONTACT_FORM)

    def get_info_cards_count(self):
        """获取信息卡片数量"""
        return len(self.find_elements(self.INFO_CARDS))

    def submit_contact_form(self, name, email, subject, message):
        """
        提交联系表单

        Args:
            name: 姓名
            email: 邮箱
            subject: 主题
            message: 消息内容
        """
        self.send_keys(self.NAME_INPUT, name)
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.SUBJECT_INPUT, subject)
        self.send_keys(self.MESSAGE_INPUT, message)
        self.click_element(self.SUBMIT_BUTTON)
        import time
        time.sleep(1)

    def is_map_visible(self):
        """检查地图是否可见"""
        return self.is_element_present(self.MAP_CONTAINER)
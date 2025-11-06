# tests/pages/about_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class AboutPage(BasePage):
    """
    关于我们页面对象
    封装关于我们页面的所有元素定位和操作
    """

    # 页面元素定位器
    PAGE_TITLE = (By.CLASS_NAME, "page-title")
    OUR_STORY_SECTION = (By.XPATH, "//h2[text()='Our Story']")
    OUR_VALUES_SECTION = (By.XPATH, "//h2[text()='Our Values']")
    OUR_TEAM_SECTION = (By.XPATH, "//h2[text()='Our Team']")
    VALUE_CARDS = (By.CLASS_NAME, "value-card")
    TEAM_MEMBERS = (By.CLASS_NAME, "team-member")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_page_title(self):
        """获取页面标题"""
        return self.get_text(self.PAGE_TITLE)

    def is_our_story_section_visible(self):
        """检查Our Story部分是否可见"""
        return self.is_element_present(self.OUR_STORY_SECTION)

    def is_our_values_section_visible(self):
        """检查Our Values部分是否可见"""
        return self.is_element_present(self.OUR_VALUES_SECTION)

    def is_our_team_section_visible(self):
        """检查Our Team部分是否可见"""
        return self.is_element_present(self.OUR_TEAM_SECTION)

    def get_value_cards_count(self):
        """获取价值观卡片数量"""
        return len(self.find_elements(self.VALUE_CARDS))

    def get_team_members_count(self):
        """获取团队成员数量"""
        return len(self.find_elements(self.TEAM_MEMBERS))
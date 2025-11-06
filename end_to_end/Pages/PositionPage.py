# tests/pages/position_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class PositionPage(BasePage):
    # 商品信息定位器
    POSITION_TITLE = (By.CLASS_NAME, "position-title")
    POSITION_IMAGE = (By.CLASS_NAME, "position-image")
    INGREDIENTS_SECTION = (By.XPATH, "//h3[text()='Ingredients:']/following-sibling::p")
    DESCRIPTION_SECTION = (By.XPATH, "//h3[text()='Description:']/following-sibling::p")
    PRICE = (By.CLASS_NAME, "price")

    # 购物车操作定位器
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(text(), 'Add to Cart')]")

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    def get_position_title(self):
        return self.get_text(self.POSITION_TITLE)

    def get_ingredients(self):
        """获取成分"""
        return self.get_text(self.INGREDIENTS_SECTION)

    def get_description(self):
        """获取描述"""
        return self.get_text(self.DESCRIPTION_SECTION)

    def get_price(self):
        """获取价格"""
        return self.get_text(self.PRICE)

    def set_quantity(self,quantity):
        self.send_keys(self.QUANTITY_INPUT,str(quantity))

    def add_to_cart(self,quantity=1):
        self.set_quantity(quantity)
        self.click_element(self.ADD_TO_CART_BUTTON)

    def is_image_visible(self):
        return self.is_element_present(self.POSITION_IMAGE)
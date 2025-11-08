# tests/pages/order_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class OrderPage(BasePage):
    # 页面元素定位器
    PAGE_TITLE = (By.CLASS_NAME, "page-title")
    BASKET_ITEMS = (By.CLASS_NAME, "basket-item")
    TOTAL_PRICE = (By.CLASS_NAME, "total-price")
    CHECKOUT_BUTTON = (By.CLASS_NAME, "btn-checkout")
    EMPTY_BASKET_MESSAGE = (By.CLASS_NAME, "empty-basket")

    # 导航链接定位器
    ACTIVE_ORDERS_LINK = (By.LINK_TEXT, "Active Orders")
    MENU_LINK = (By.LINK_TEXT, "Go to Menu")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_page_title(self):
        """获取页面标题"""
        return self.get_text(self.PAGE_TITLE)

    def get_basket_items_count(self):
        return len(self.find_elements(self.BASKET_ITEMS))

    def get_total_price(self):
        """获取总价"""
        return self.get_text(self.TOTAL_PRICE)

    def place_order(self):
        """下订单"""
        self.click_element(self.CHECKOUT_BUTTON)
        import time
        time.sleep(1)
        from .MyOrderPage import MyOrderPage
        return MyOrderPage(self.driver)

    def is_basket_empty(self):
        """检查购物车是否为空"""
        return self.is_element_present(self.EMPTY_BASKET_MESSAGE)

    def navigate_to_active_orders(self):
        """导航到活跃订单"""
        self.click_element(self.ACTIVE_ORDERS_LINK)
        import time
        time.sleep(1)
        from .MyOrdersPage import MyOrdersPage
        return MyOrdersPage(self.driver)

    def navigate_to_menu(self):
        """导航到菜单"""
        self.click_element(self.MENU_LINK)
        from .MenuPage import MenuPage
        return MenuPage(self.driver)
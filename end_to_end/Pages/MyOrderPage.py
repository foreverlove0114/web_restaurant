# tests/pages/my_order_page.py
import time

from dotenv import set_key
from selenium.webdriver.common.by import By
from .BasePage import BasePage


class MyOrderPage(BasePage):
    """
    订单详情页面对象
    封装单个订单详情页面的所有元素定位和操作
    """

    # 页面元素定位器
    ORDER_TITLE = (By.TAG_NAME, "h2")
    ORDER_ITEMS = (By.CSS_SELECTOR, "ul li")
    ORDER_TIME = (By.XPATH, "//p[contains(., 'Date & Time:')]")
    TOTAL_PRICE = (By.XPATH, "//p[contains(., 'UAH')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(., 'Cancel Order')]")
    ORDER_ITEMS_LIST = (By.CSS_SELECTOR, "ul tr")  # 根据实际HTML结构调整

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_order_title(self):
        """获取订单标题"""
        return self.get_text(self.ORDER_TITLE)

    def get_order_id(self):
        """从标题中提取订单ID"""
        title = self.get_order_title()
        if "Order №" in title:
            import re
            match = re.search(r'Order №(\d+)', title)
            if match:
                return match.group(1)
        return None

    def get_order_items_count(self):
        """获取订单商品数量"""
        return len(self.find_elements(self.ORDER_ITEMS))

    def get_order_time(self):
        """获取订单时间"""
        if self.is_element_present(self.ORDER_TIME):
            time_text = self.get_text(self.ORDER_TIME)
            # 提取时间部分
            if "Date & Time:" in time_text:
                return time_text.replace("Date & Time:", "").strip()
        return None

    def get_total_price(self):
        """获取总价"""
        if self.is_element_present(self.TOTAL_PRICE):
            price_text = self.get_text(self.TOTAL_PRICE)
            # 提取价格部分
            if "Total Price:" in price_text:
                print(price_text)
                return price_text.replace("Total Price:", "").strip()
        return None

    def get_order_items_details(self):
        """
        获取订单商品详情

        Returns:
            list: 包含商品信息的字典列表
        """
        items = self.find_elements(self.ORDER_ITEMS_LIST)
        order_items = []

        for item in items:
            # 根据实际HTML结构解析商品信息
            cells = item.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:  # 假设有4列：名称、数量、单价、总价
                item_info = {
                    'name': cells[0].text,
                    'quantity': cells[1].text,
                    'price': cells[2].text,
                    'total': cells[3].text
                }
                order_items.append(item_info)

        return order_items

    def is_cancel_button_present(self):
        """检查取消订单按钮是否存在"""
        return self.is_element_present(self.CANCEL_BUTTON)

    def cancel_order(self):
        if self.is_cancel_button_present():
            self.click_element(self.CANCEL_BUTTON)
            import time
            time.sleep(1)
            from .MyOrdersPage import MyOrdersPage
            return MyOrdersPage(self.driver)
        else:
            raise Exception("取消订单按钮不存在")

    def get_order_summary(self):
        return {
            'order_id': self.get_order_id(),
            'title': self.get_order_title(),
            'order_time': self.get_order_time(),
            'total_price': self.get_total_price(),
        }
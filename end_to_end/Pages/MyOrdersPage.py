# tests/pages/my_orders_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage


class MyOrdersPage(BasePage):
    """
    我的订单列表页面对象
    封装订单列表页面的所有元素定位和操作
    """

    # 页面元素定位器
    PAGE_TITLE = (By.TAG_NAME, "h2")
    ORDER_ITEMS = (By.CLASS_NAME, "order-item")
    EMPTY_ORDERS_MESSAGE = (By.CLASS_NAME, "empty-orders")
    VIEW_DETAILS_LINKS = (By.LINK_TEXT, "View Details")
    ORDER_INFO = (By.CSS_SELECTOR, ".order-item p")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_page_title(self):
        """获取页面标题"""
        return self.get_text(self.PAGE_TITLE)

    def get_orders_count(self):
        """获取订单数量"""
        return len(self.find_elements(self.ORDER_ITEMS))

    def is_empty_orders_message_displayed(self):
        """检查空订单消息是否显示"""
        return self.is_element_present(self.EMPTY_ORDERS_MESSAGE)

    def get_empty_orders_message(self):
        """获取空订单消息文本"""
        if self.is_empty_orders_message_displayed():
            return self.get_text(self.EMPTY_ORDERS_MESSAGE)
        return None

    def view_order_details(self, index=0):
        """
        查看订单详情

        Args:
            index: 订单索引

        Returns:
            MyOrderPage: 订单详情页面对象
        """
        links = self.find_elements(self.VIEW_DETAILS_LINKS)
        if index < len(links):
            # 点击前先滚动到元素
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", links[index])
            links[index].click()
            from .MyOrderPage import MyOrderPage
            return MyOrderPage(self.driver)
        return None

    def get_order_info(self, index=0):
        """
        获取订单信息

        Args:
            index: 订单索引

        Returns:
            dict: 包含订单信息的字典
        """
        items = self.find_elements(self.ORDER_ITEMS)
        if index < len(items):
            order_text = items[index].text
            # 解析订单文本获取有用信息
            lines = order_text.split('\n')
            return {
                'raw_text': order_text,
                'lines': lines
            }
        return None

    def get_all_orders_info(self):
        """获取所有订单信息"""
        orders = self.find_elements(self.ORDER_ITEMS)
        orders_info = []

        for order in orders:
            order_text = order.text
            lines = order_text.split('\n')
            orders_info.append({
                'raw_text': order_text,
                'lines': lines
            })

        return orders_info

    def is_order_present(self, order_id):
        """
        检查指定订单是否存在

        Args:
            order_id: 订单ID

        Returns:
            bool: 如果订单存在返回True
        """
        orders_info = self.get_all_orders_info()
        for order_info in orders_info:
            if f"Order №{order_id}" in order_info['raw_text']:
                return True
        return False
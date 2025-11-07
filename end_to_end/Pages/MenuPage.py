# tests/pages/menu_page.py
from selenium.webdriver.common.by import By
from .BasePage import BasePage

class MenuPage(BasePage):
    # 页面元素定位器
    PAGE_TITLE = (By.CLASS_NAME, "page-title")
    SEARCH_INPUT = (By.NAME, "q")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(text(), 'Search')]")
    MENU_ITEMS = (By.CLASS_NAME, "menu-item")
    MENU_ITEM_NAME = (By.TAG_NAME, "h3")
    MENU_ITEM_PRICE = (By.CLASS_NAME, "price")
    DETAILS_BUTTON = (By.LINK_TEXT, "More Details")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def search_menu_items(self,query):
        print(f"开始搜索")
        self.send_keys(self.SEARCH_INPUT, query)
        self.click_element(self.SEARCH_BUTTON)

    def get_menu_items_count(self):
        import time
        time.sleep(1)
        return len(self.find_elements(self.MENU_ITEMS))

    def get_menu_item_info(self, index=0):
        items = self.find_elements(self.MENU_ITEMS)
        if index < len(items):
            item = items[index]
            name = item.find_element(*self.MENU_ITEM_NAME).text
            price = item.find_element(*self.MENU_ITEM_PRICE).text
            return{
                "name":name,
                "price":price
            }
        return None

    def view_item_details(self,index=0):
        items = self.find_elements(self.MENU_ITEMS)
        if index<len(items):
            try:
                details_button = items[index].find_element(*self.DETAILS_BUTTON)
                details_button.click()

                import time
                time.sleep(1)

                from .PositionPage import PositionPage
                return PositionPage(self.driver)
            except Exception:
                # 处理找不到按钮的情况
                return None
        return None

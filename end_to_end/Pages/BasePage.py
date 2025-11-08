import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.sql.base import elements


class BasePage:

    def __init__(self,driver):
        print(f"🔧 BasePage 初始化，接收到 driver: {id(driver)}")
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.long_wait = WebDriverWait(driver, 15)  # 添加长等待

    def find_element(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self,locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self,locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self,locator,text):
        element = self.find_element(locator)
        element.clear()
        time.sleep(1)
        element.send_keys(text)

    def get_text(self,locator):
        return self.find_element(locator).text
        import time
        time.sleep(2)

    def is_element_present(self,locator):
        try:
            self.find_element(locator)
            return True
        except:
            return False

    def wait_for_element_visible(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return self.wait.until(EC.visibility_of_element_located(locator))

    def scroll_to_element(self,locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def take_screenshot(self,filename):
        self.driver.save_screenshot(filename)
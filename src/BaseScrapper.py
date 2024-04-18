

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

class BaseScrapper:
    def __init__(self, logging):
        self.driver = None
        self.sec_driver = None
        #self.elements = None
        self.status = None
        self.logging = logging
        #self.link_ctr = 0
        #self.links = None

    def start_driver(self):
        if self.status is None:
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--headless')
            self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
            self.sec_driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
            self.status = True

    def get_status(self):
        return self.status

    def stop_driver(self):
        if self.status is True:
            self.driver.quit()
            self.sec_driver.quit()
            self.logging.info("Selenium successfully disconnected from the website")

    def extract_data(self, tag, xpath, extract_type='text'):
        if self.status is False:
            return None
        try:
            element = self.sec_driver.find_element(By.XPATH, xpath)
            if extract_type == 'text':
                return element.text.strip()
            elif extract_type == 'text_split':
                return element.text.strip().split('\n')[0]
            elif extract_type == 'url':
                return element.get_attribute('href')
            else:
                self.logging.error(f"Unknown extract type: {extract_type} at tag: {tag}")
                return None
        except Exception as e:
            self.logging.error(f"Error: {e} at tag: {tag}")
            return None

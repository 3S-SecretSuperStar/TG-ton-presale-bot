

import time
import logging
# from bs4 import BeautifulSoup
from src.TokenData import TokenData
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.BaseScrapper import BaseScrapper

class SolanaPadScrapper(BaseScrapper):
    def __init__(self, logging):
        super().__init__(logging)
        self.url = None
        self.elements = None
        #self.status = None
        #self.logging= logging
        #self.link_ctr = 0
        self.links = []

    def extract_token_info_strategy1(self, url):

        super().start_driver()
        # status, live_status = self.open_sub_url(url=url, xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]")
        
        # if status == False:
        #     return data
        
        data = TokenData()
        try:            
            self.sec_driver.get(url)
            self.sec_driver.implicitly_wait(10)           
            status = True
        except Exception as ex:
            status = False
            self.logging.error("Exception (%s) occured while Opening URL %s", ex, url)

        if status == True:
            
            data.status = True
            data.symbol = super().extract_data(tag='Symbol', xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/h3", extract_type='text')                
            data.live_status = super().extract_data(tag='Live Status', xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/span", extract_type='text')
            data.web = super().extract_data(tag='URL', xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/a[1]", extract_type='url')
            data.twitter = super().extract_data(tag='Twitter', xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/a[2]", extract_type='url')
            data.telegram = super().extract_data(tag='Telegram', xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/a[3]", extract_type='url')
           
            data.rate       = super().extract_data(tag="Current Rate\n",      xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]", extract_type='text').split('\n')[1]
            data.start_time  = super().extract_data(tag="Start Time\n", xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[2]", extract_type='text').split('\n')[1]
            data.end_time    = super().extract_data(tag="End Time\n",   xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[3]", extract_type='text').split('\n')[1]
            data.soft_cap    = super().extract_data(tag="Soft Cap\n",   xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[4]", extract_type='text').split('\n')[1]
            
            data.raised = super().extract_data(tag="\n", xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div/span[1]", extract_type='text_split').split('\n')[0]   
            data.token_address = super().extract_data(tag="Token Address\n", xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[9]/div/span[1]", extract_type='text')
            data.pool_address = super().extract_data(tag="Pool Address\n", xpath="/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[10]/div/span[1]", extract_type='text')
        return data
            
    def get_Status(self):
        return self.status
    
    def get_links(self):
        url = "https://solanapad.io/launchpad-list"
        super().start_driver()
        self.driver.get(url)

        # element = WebDriverWait(self.driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div/ul/li[4]/span/span"))
        # )
        # time.sleep(3)
        # element.click()

        
        #Wait for the element to be clickable
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div/ul/li[3]/span/span"))
        )
        time.sleep(10)
        # Click on the element
        element.click()
        

        base_xpath = "/html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[{}]"
        # /html/body/div/div[1]/div[2]/main/div/div[2]/div[2]/div[{}]
        # /html/body/div/div[1]/div[2]/main/div/div[2]/div[3]/div
        #elements = self.driver.find_elements(By.XPATH, "/html/body/div/div[1]/div[2]/main/div/div[2]/div[3]")

        try:
            single_xpath = "/html/body/div/div[1]/div[2]/main/div/div[2]/div[3]/div"
            #element = self.driver.find_element(By.XPATH, xpath)
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, single_xpath))
            )
            #self.driver.implicitly_wait(5)
            if element.is_displayed():
                child_element = element.find_element(By.XPATH, "div[7]/div[2]/a")
                link = child_element.get_attribute('href')
                self.links.append(link)
            
            # Process the element here (e.g., scrape its text or attributes)
            print("Element", 0, "text:", element.text)
        except:
            # If the element is not found, break the loop
            print('Exception accessing 0th element')

        # Loop through a range of numbers to generate XPaths dynamically
        for i in range(1, 100):  # Assuming a maximum of 100 entries, adjust as needed
            # Construct the XPath for the current entry
            xpath = base_xpath.format(i)
            
            # Find the element using the generated XPath
            try:
                #element = self.driver.find_element(By.XPATH, xpath)
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                #self.driver.implicitly_wait(5)
                if element.is_displayed():
                    child_element = element.find_element(By.XPATH, "div[7]/div[2]/a")
                    link = child_element.get_attribute('href')
                    self.links.append(link)
                
                # Process the element here (e.g., scrape its text or attributes)
                print("Element", i, "text:", element.text)
            except:
                # If the element is not found, break the loop
                break

        return self.links

# /html/body/div/div[1]/div[2]/main/div/div[2]/div[3]
# /html/body/div/div[1]/div[2]/main/div/div[2]/div[3]/div[1]
# /html/body/div/div[1]/div[2]/main/div/div[2]/div[3]/div[2]
# /html/body/div/div[1]/div[2]/main/div/div[2]/div[3]/div[3]

    # def decode_xpath(self, html_content):
    #     # Parse the HTML content
    #     soup = BeautifulSoup(html_content, 'html.parser')

    #     # Extracting Twitter link
    #     twitter_link = soup.find('a', href=lambda href: href and 'twitter.com' in href)['href']
  



if __name__ == "__main__":
    scraper = SolanaPadScrapper(logging)
    links = scraper.get_links()
    for link in links:
        status = scraper.extract_token_info_strategy1(url=link)
        #status = scraper.extract_token_info_strategy1(url="https://solanapad.io/launchpad-list/3wLDvfT9Gm4fp2mqHhcWouf1QFMLUCGSR8MrDvBbYSnK")
    print("Status: ", status)
   

        
    # links = scraper.get_links()
    # for link in links:
    #     print(link.get_attribute('href'))
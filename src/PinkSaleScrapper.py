
import logging
from src.TokenData import TokenData
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.BaseScrapper import BaseScrapper

class PinkSaleScrapper(BaseScrapper):
    def __init__(self, logging):
        super().__init__(logging)
        self.url = "https://www.pinksale.finance/solana/launchpad"
        #self.elements = None
        self.links = []
        self.logging = logging

    def start_driver(self):
        super().start_driver()
        
        try:            
            self.driver.get(self.url)
            self.driver.implicitly_wait(10)
            # self.elements = self.driver.find_elements(By.CLASS_NAME, "flex-1.overflow-x-auto")
            # self.links = self.elements[0].find_elements(By.TAG_NAME, 'a')
            # self.status = True
            # self.logging.info("Selenium successfully connected to the website")
            self.status = True
        except Exception as ex:
            self.status = False
            self.logging.error("Exception (%s) occured while Opening URL %s", ex, self.url)
        

        if self.status == True:
            try:                
                elements = self.driver.find_elements(By.CLASS_NAME, "flex-1.overflow-x-auto")
                links = elements[0].find_elements(By.TAG_NAME, 'a')

                for link in links:                    
                    proj_url = link.get_attribute('href')
                    self.logging.info('URL: %s', proj_url)
                    self.links.append(proj_url)
                self.status = True
                self.logging.info("Selenium successfully connected to the website")            
            except Exception as ex:
                self.status = False
                self.logging.error("Error connecting to the database: %s", ex)            
        return self.status
            
    def get_Status(self):
        return self.status
    
    def get_links(self):
        return self.links

    def extract_token_info(self, proj_url):
        data = self.extract_token_info_strategy1(proj_url)
        if data.live_status == True:            
            return data
        
        data = self.extract_token_info_strategy2(proj_url)
        if data.live_status == True:
            return data
        else:
            return data
    

    # def get_next_project_stats(self):
    #     id = 0
    #     for link in self.links:
    #         if id < self.links_ctr:
    #             id = id + 1
    #             continue
            
    #         self.link_ctr = self.link_ctr + 1
    #         proj_url = link.get_attribute('href')
    #         print(link.get_attribute('href'))  # Print the href attribute value of each <a> tag
    #         data = self.extract_token_info(proj_url)
    #         return data

    # def extract_text(self, tag, xpath):
    #     try:
    #         element = self.sec_driver.find_element(By.XPATH, xpath)
    #         return element.text.strip() 
    #     except Exception as e:
    #         logging.error("Error:", e, " at tag :", tag)
    #         return None
    
    # def extract_url(self, tag, xpath):
    #     try:
    #         element = self.sec_driver.find_element(By.XPATH, xpath)
    #         return element.get_attribute('href')        
    #     except Exception as e:
    #         logging.error("Error:", e, " at tag :", tag)
    #         return None


    def open_sub_url(self, url, xpath):        
        # Set the maximum time to wait for elements to be loaded (in seconds)
        timeout = 50
        retries = 3
        status = False
        live_status = None
        
        # Set implicit wait time for elements to be located
        self.sec_driver.implicitly_wait(10)
        
        try:
            # Attempt to open the URL
            self.sec_driver.get(url)
        except Exception as e:
            # Log any exceptions during URL opening
            self.logging.error(f"Failed to open URL: {url}. Exception: {e}")
            return status, live_status

        # Retry mechanism to handle page loading failures
        while retries > 0:
            retries -= 1
            try:
                # Wait until the element with class "mb-4" is present, indicating page load
                WebDriverWait(self.sec_driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "mb-4")))
                
                # Extract live status information from the page
                live_status = super().extract_data("live_status", xpath=xpath)

                # If live status is successfully extracted, set status to True and exit loop
                if live_status is not None:
                    status = True
                    self.logging.info(f"Page {url} loaded successfully.")
                    break               


            except Exception as ex:
                # Log any exceptions during page loading
                self.logging.error(f"Exception occurred while loading page at URL: {url}. Exception: {ex}")

        self.sec_driver.implicitly_wait(10)
        return status, live_status

    def extract_token_info_strategy1(self, url):
        data = TokenData()
       
        # Open URL and Extract Live Status
        status, live_status = self.open_sub_url(url=url, xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]")
        if status == False:
            return data
        
        data.status = True
        
        if 'live' not in live_status.lower():            
            return data
        
        # Set Live Status to True
        data.live_status = True

        # Extract Current Rate 
        data.rate = super().extract_data( tag="current_rate", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[2]/div[1]/div[3]/div[4]/div[2]")
        
        # Extract Current Raised
        data.raised = super().extract_data( tag="current_raised", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[2]/div[1]/div[3]/div[5]/div[2]")
        
        # Extract web, twitter and telegram addresses
        data.web = super().extract_data(tag="web_address", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/a[1]", extract_type="url")
        data.twitter = super().extract_data(tag="twitter_address", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/a[2]", extract_type="url")
        data.telegram = super().extract_data(tag="telegram_address", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/a[3]", extract_type="url")

        # Extract Address
        data.token_address = super().extract_data(tag="token_address", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]", extract_type="text_split")

        # Extract name, symbol, supply
        data.name = super().extract_data(tag="name", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[2]/div/div[3]/div[2]")
        data.symbol = super().extract_data(tag="symbol", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[2]/div/div[4]/div[2]")
        data.supply = super().extract_data(tag="total_supply", xpath="/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[2]/div/div[6]/div[2]")

        # Extract Pool Address
        data.pool_address = super().extract_data("pool_address", "/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[2]", extract_type="text_split")

        # Extract soft cap
        data.soft_cap = super().extract_data("soft_cap", "/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[5]/div[2]")
        
        # Extract start, end and lock up time
        data.start_time = super().extract_data("start_time", "/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[6]/div[2]")
        data.end_time = super().extract_data("end_time", "/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[7]/div[2]")
        data.lockup_time = super().extract_data("lockup_time", "/html/body/div/div/div[3]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[10]/div[2]")

        return  data
    
    def extract_token_info_strategy2(self, url):
        data = TokenData()
       
        # Open URL and Extract Live Status
        status, live_status = self.open_sub_url(url=url, xpath="/html/body/div/div/div[3]/main/div/div/div[1]/div[2]/div[3]/div[2]/div[2]/div")
        if status == False:
            return data
        
        data.status = True
        
        if 'live' not in live_status.lower():            
            return data
        
        # Set Live Status to True
        data.live_status = True

        # Extract Current Rate 
        data.rate = super().extract_data( "current_rate", "/html/body/div/div/div[3]/main/div/div/div[1]/div[2]/div[3]/div[5]/div[2]/div")
        
        # Extract Current Raised
        data.raised = super().extract_data( "current_raised", "/html/body/div/div/div[3]/main/div/div/div[1]/div[2]/div[3]/div[6]/div[2]/div")
        
        # Extract web, twitter and telegram addresses
        data.web = super().extract_data("web_address", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/a[1]", extract_type="url")
        data.twitter = super().extract_data("twitter_address", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/a[2]", extract_type="url")
        data.telegram = super().extract_data("telegram_address", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]/a[3]", extract_type="url")

        # Extract Address
        data.token_address = super().extract_data("token_address", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]", extract_type="text_split")

        # Extract name, symbol, supply
        data.name = super().extract_data("name", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]/div")
        data.symbol = super().extract_data("symbol", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div[2]")
        data.supply = super().extract_data("total_supply", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[2]/div/div[6]/div[2]/div")

        # Extract Pool Address
        data.pool_address = super().extract_data("pool_address", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]", extract_type="text_split")

        # Extract soft cap
        data.soft_cap = super().extract_data("soft_cap", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[3]/div[6]/div[2]")
        
        # Extract start, end and lock up time
        data.start_time = super().extract_data("start_time", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[3]/div[7]/div[2]")
        data.end_time = super().extract_data("end_time", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[3]/div[8]/div[2]")
        data.lockup_time = super().extract_data("lockup_time", "/html/body/div/div/div[3]/main/div/div/div[1]/div[1]/div[1]/div[3]/div[12]/div[2]")

        return  data
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = PinkSaleScrapper(logging)
    status = scraper.start_driver()
    if status:
        links = scraper.get_links()
        for link in links:
            print(link)
            scraper.extract_token_info(link)

    scraper.close_driver()
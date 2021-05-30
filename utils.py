from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(level=logging.WARNING)

class Utils:
    # def __init__(self):
    #     #headless option to chromedriver
    #     self.chrome_options = Options()
    #     self.chrome_options.add_argument("--headless")
    #     self.chrome_options.add_argument('--log-level=3')

    #     #webdriver get source
    #     self.driver = webdriver.Chrome(chrome_options=self.chrome_options)


    def get_url_content(self, url_link, page_number=None, **filters):
        """
        Get source code frome page
        """
        #headless option to chromedriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--log-level=3')

        #webdriver get source
        driver = webdriver.Chrome(chrome_options=chrome_options)

        if page_number:
            url_link += f"?page={page_number}"

        for key, value in filters.items():
            url_link += self.get_search_filter(key, value)
        

        driver.get(url_link)
        page_source = driver.page_source


        soup = BeautifulSoup(page_source, "html.parser")
        driver.close()

        return soup, url_link

    def check_page_content(self, soup):
        """
        Return false when nothing meets criteria
        """
        if soup.find(class_="emptynew" ) == None:
            return True
        
        return False

    def get_page_count(self, soup):
        """
        Return number of pages
        """
        pager = soup.find(class_="pager")

        if pager == None: 
            return 1
        
        pager_items = pager.find_all(class_="item")

        return int(pager_items[-1].get_text() )

    def get_page_links(self, soup):
        """
        Gets all links from one site and return them into a list
        """
        if self.check_page_content(soup) == False:
            return None
        
        offers = soup.find_all(class_="offer-wrapper")
        links = [offer.find("a").get("href") for offer in offers if offer.find("a").get("href") != "#"]

        return links

    def reduce_duplicates(self, list_of_offers):
        """
        Reduce duplicated offers
        """

        return list(set(list_of_offers))

    def txt_to_float(self, text):
        """
        Parse number in text from olx offer to float
        """
        parsed = float("".join(text.replace(",",".").split(" ")[:-1]))

        return parsed

    def get_search_filter(self, filter_name, filter_value):
        """
        Get filters
        """
        if filter_name == "localization":
            value = f"{filter_value}/?"
        if filter_name == "surface_min":
            value = f"search%5Bfilter_float_m%3Afrom%5D={filter_value}&"
        if filter_name == "surface_max":
            value = f"search%5Bfilter_float_m%3Ato%5D={filter_value}&"
        if filter_name == "seller":
            if filter_value == "all":
                value = ""
            else:
                value = f"search%5Bprivate_business%5D={filter_value}&"
        if filter_name == "type":
            value = f"search%5Bfilter_enum_type%5D%5B0%5D={filter_value}&"

        return value

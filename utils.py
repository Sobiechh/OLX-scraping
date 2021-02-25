from bs4 import BeautifulSoup
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TEST_URL1 = "https://www.olx.pl/nieruchomosci/dzialki/lodzkie/"
TEST_URL2 = "https://www.olx.pl/nieruchomosci/dzialki/tomaszow-mazowiecki/?search%5Bfilter_float_price%3Ato%5D=1"
TEST_URL3 = "https://www.olx.pl/nieruchomosci/dzialki/lodzkie/?search%5Bfilter_float_m%3Ato%5D=200"
TEST_URL4 = "https://www.olx.pl/nieruchomosci/dzialki/lodzkie/?search%5Bfilter_float_price%3Ato%5D=50000"

current_page_number = 1

def get_url_content(url_link, page_number):
    """
    Get source code frome page
    """

    if page_number != None:
        url_link += f"&page={page_number}"
    
    #headless option to chromedriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    #webdriver get source
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url_link)
    page_source = driver.page_source


    html_parser = BeautifulSoup(page_source, "html.parser")
    driver.close()

    return html_parser

def check_page_content(soup):
    """
    Return false when nothing meets criteria
    """
    if soup.find(class_="emptynew" ) == None:
        return True
    
    return False

def get_page_count(url_criteria):
    """
    Return number of pages
    """
    soup = get_url_content(url_criteria, 1)
    pager = soup.find(class_="pager")

    if pager == None: 
        return 1
    
    pager_items = pager.find_all(class_="item")
    numbers = [num.find('span').get_text() for num in pager_items]

    return int(numbers[-1])

def get_page_links(soup):
    """
    Gets all links from one site and return them into a list
    """
    if check_page_content(soup) == False:
        return None
    
    offers = soup.find_all(class_="offer-wrapper")
    links = [offer.find("a").get("href") for offer in offers if offer.find("a").get("href") != "#"]

    return links

def get_all_offers(url_criteria):
    """
    Get all links offer from all sites
    """
    num_of_sites = get_page_count(url_criteria)

    all_offers = []

    for page_number in range(1, num_of_sites+1):
        url_content = get_url_content(url_criteria, page_number)
        page_links = get_page_links(url_content)

        if page_links == None:
            return []

        all_offers.extend(page_links)
    
    return reduce_duplicates(all_offers)

def reduce_duplicates(list_of_offers):
    """
    Reduce duplicated offers
    """
    print(list(set(list_of_offers)))
    return list(set(list_of_offers))

def txt_to_float(text):
    """
    Parse number in text from olx offer to float
    """
    parsed = float("".join(text.replace(",",".").split(" ")[:-1]))

    return parsed
from bs4 import BeautifulSoup
import logging
import requests

TEST_URL1 = "https://www.olx.pl/nieruchomosci/dzialki/lodzkie/"
TEST_URL2 = "https://www.olx.pl/nieruchomosci/dzialki/tomaszow-mazowiecki/?search%5Bfilter_float_price%3Ato%5D=1"
TEST_URL3 = "https://www.olx.pl/nieruchomosci/dzialki/lodzkie/?search%5Bfilter_float_m%3Ato%5D=200"

def get_url_content(url_link):
    page = requests.get(url_link)
    html_parser = BeautifulSoup(page.content, "html.parser")

    return html_parser

def check_page_content(soup):
    if soup.find(class_="emptynew" ) == None:
        return True
    return False

def get_page_count(soup):
    pager = soup.find(class_="pager")
    if pager == None: 
        return
    
    pager_items = pager.find_all(class_="item")
    nums = [num.find('span').get_text() for num in pager_items]

    return int(nums[-1])

def get_offer_links(soup):

    if check_page_content(soup) == False:
        return None
    
    offers = soup.find_all(class_="wrap")
    links = [offer.find("a").get("href") for offer in offers if offer.find("a").get("href") != "#"]

    return links

    

odp = get_url_content(TEST_URL1)
print(get_offer_links(odp))
odp = get_url_content(TEST_URL2)
print(get_offer_links(odp))
odp = get_url_content(TEST_URL3)
print(get_offer_links(odp))
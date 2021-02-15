from bs4 import BeautifulSoup
import logging
import requests

TEST_URL1 = "https://www.olx.pl/nieruchomosci/dzialki/lodzkie/"
TEST_URL2 = "https://www.olx.pl/nieruchomosci/dzialki/tomaszow-mazowiecki/?search%5Bfilter_float_price%3Ato%5D=1"
TEST_URL3 = "https://www.olx.pl/nieruchomosci/dzialki/lodzkie/?search%5Bfilter_float_m%3Ato%5D=200"

current_page_number = 1

def get_url_content(url_link, page_number):
    """
    Get all html code frome page
    """
    page_number_url = f"/?page={page_number}"
    page = requests.get(url_link+page_number_url)
    html_parser = BeautifulSoup(page.content, "html.parser")

    return html_parser

def check_page_content(soup):
    """
    Return false when nothing meets criteria
    """
    if soup.find(class_="emptynew" ) == None:
        return True
    return False

def get_page_count(soup):
    """
    Return number of pages
    """
    pager = soup.find(class_="pager")
    if pager == None: 
        return 1
    
    pager_items = pager.find_all(class_="item")
    numbers = [num.find('span').get_text() for num in pager_items]

    print(numbers)
    return int(numbers[-1])

def get_page_links(soup):
    """
    Gets all links from one site and return them into a list
    """
    if check_page_content(soup) == False:
        return None
    
    offers = soup.find_all(class_="wrap")
    links = [offer.find("a").get("href") for offer in offers if offer.find("a").get("href") != "#"]

    return links

def get_all_offers(url_criteria):
    """
    Get all links offer from all sites
    """
    url_content = get_url_content(url_criteria, current_page_number)
    num_of_sites = get_page_count(url_content)

    all_offers = []

    for page_number in range(1, num_of_sites+1):
        url_content = get_url_content(url_criteria, page_number)
        page_links = get_page_links(url_content)
        all_offers.extend(page_links)
    
    return reduce_promoted(all_offers)

def reduce_promoted(list_of_offers):
    """
    Reduce ';promoted' from link to avoid duplicates
    """
    for index, link in enumerate(list_of_offers):
        if ";promoted" in link:
            list_of_offers[index] = link.split(";")[0]

    return list_of_offers

#tests
odp = get_all_offers(TEST_URL3)
print(len(odp))
odp = get_all_offers(TEST_URL2)
print(len(odp))
odp = get_all_offers(TEST_URL3)
print(len(odp))


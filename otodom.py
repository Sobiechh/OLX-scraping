from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from utils import get_url_content, txt_to_float

"""
Get content from otodom page
"""
TEST_URL = "https://www.otodom.pl/pl/oferta/malanow-promocja-dzialki-budowlane-ID3Z50c.html?"
TEST_URL2 ="https://www.otodom.pl/pl/oferta/dzialka-projekt-pozwolenie-na-budowe-fak-vat-ID49gOh.html#08fbc89bdc"


def get_offer_id(soup):
    
    offer_id_desc = soup.find("div", {"class" : "css-jjerc6 edhdn7k3"})
    offer_id = int(offer_id_desc.text.split(" ")[-1])

    return offer_id
    

def get_offer_surface(soup):

    surface_txt = soup.find("div", {"class" : "css-1ytkscc ecjfvbm0"})
    surface = txt_to_float(surface_txt.text)

    return surface

def get_offer_title(soup):

    title = soup.find("h1", {"class" : "css-46s0sq edo911a18"})

    return title.text

def get_offer_localization(soup):

    localization_name = soup.find("a", {"class" : "css-1qz7z11 eom7om61"})
    localization_name = localization_name.text.split(",")[0].strip()

    return localization_name

def get_offer_description(soup):

    description =  soup.find("div", {"data-cy" : "adPageAdDescription"})
    
    return description.text

def get_offer_price(soup):

    price_txt = soup.find("strong", {"data-cy" : "adPageHeaderPrice"})

    price = txt_to_float(price_txt.text)

    return price

def get_offer_infos(url):
    soup = get_url_content(url, None)

    offer_id = get_offer_id(soup)
    offer_surface = get_offer_surface(soup)
    offer_title = get_offer_title(soup)
    offer_localization = get_offer_localization(soup)
    offer_descritpion = get_offer_description(soup)
    offer_price = get_offer_price(soup)

    details = {
        "id": offer_id,
        "surface": offer_surface,
        "title": offer_title,
        "localization": offer_localization,
        "description": offer_descritpion,
        "price": offer_price
    }

    return details

details = get_offer_infos(TEST_URL)
details2 = get_offer_infos(TEST_URL2)

print(details)
print(details2)
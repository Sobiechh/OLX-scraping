from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

"""
Get content from otodom page
"""
TEST_URL = "https://www.otodom.pl/pl/oferta/malanow-promocja-dzialki-budowlane-ID3Z50c.html?"
TEST_URL2 ="https://www.otodom.pl/pl/oferta/dzialka-projekt-pozwolenie-na-budowe-fak-vat-ID49gOh.html#08fbc89bdc"


def get_offer_id(bottom_bar):
    offer_id = bottom_bar[-1].find("strong").get_text()

    return offer_id

def get_details(soup):
    offer_details = soup.find_all(class_="offer-details__item")

    return offer_details
    
def get_offer_surface(details):
    surface_txt = details[2].find("strong").get_text()

    surface = txt_to_float(surface_txt)

    return surface

def get_offer_title(soup):
    title = soup.find(class_='offer-titlebox').find('h1').get_text().strip()

    return title

def get_offer_localization(soup):
    localization_name = soup.find(class_='offer-user__address').p.get_text().split(',')[0].strip()
    
    return localization_name

def get_offer_description(soup):
    description =  soup.find(id='textContent').get_text().strip()
    
    return description

def get_offer_price(soup):
    price_txt = soup.find(class_="pricelabel__value arranged").get_text()

    price = txt_to_float(price_txt)

    return price

def txt_to_float(text):
    """
    Parse number in text from olx offer to float
    """
    parsed = float("".join(text.replace(",",".").split(" ")[:-1]))

    return parsed

def get_offer_infos(url):
    page = requests.get(TEST_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    bottom_bar = get_bottom_bar(soup)
    details = get_details(soup)

    """
    offer_id -> get from bottom bar
    offer_surfacet -> get from details at the top of page
    """
    offer_id = get_offer_id(bottom_bar)
    offer_surface = get_offer_surface(details)

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

def get_bottom_bar(soup):
    # bottom_bar = soup.find_all(lambda tag: tag.name == 'div')
    #and tag.get('class') == ['z']

    bottom_bar = soup.select("div.css-y2xgt6.et0r0y90")

    return bottom_bar


# page = requests.get(TEST_URL)

# soup = BeautifulSoup(page.content, "html.parser")


driver = webdriver.Chrome()
driver.get(TEST_URL)
c = driver.page_source
soup = BeautifulSoup(c, "html.parser")

# with open("wynik.txt") as file:
#     file.write(soup)

get_element  = bottom_bar = soup.find_all("div", {"class" : "css-jjerc6 edhdn7k3"})
print(get_element)

driver.close()

# print(get_bottom_bar(soup))
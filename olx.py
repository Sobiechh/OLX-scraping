from bs4 import BeautifulSoup
import requests

"""
Get content from olx page
"""
TEST_URL = "https://www.olx.pl/oferta/dzialka-pod-farme-fotowoltaiczna-CID3-IDFMtbN.html#b45bf9918b"
TEST_URL2 ="https://www.olx.pl/oferta/sprzedam-dzialke-w-rod-ksiezy-mlyn-CID3-IDIlPPY.html#3971846459;promoted"

def get_bottom_bar(soup):
    bottom_bar = soup.find_all(class_="offer-bottombar__item")

    return bottom_bar

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
    page = requests.get(url)
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

print(get_offer_infos(TEST_URL))
print(get_offer_infos(TEST_URL2))
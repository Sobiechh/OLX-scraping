from utils import txt_to_float

"""
Get content from olx page
"""

def get_bottom_bar(soup):
    bottom_bar = soup.find(class_="css-1v2fuie")

    return bottom_bar

def get_offer_id(bottom_bar):
    offer_id = bottom_bar.find(class_="css-7oa68k-Text").get_text()
    
    return int(offer_id.split(' ')[-1])

def get_details(soup):
    offer_details = soup.find(class_="css-sfcl1s")

    return offer_details
    
def get_offer_surface(details):
    details_items = details.find_all(class_="css-ox1ptj")
    surface_txt = details_items[-2].get_text().split(' ', 1)[-1]
    surface = txt_to_float(surface_txt)

    return surface

def get_offer_title(soup):
    title = soup.find('h1', {"data-cy": "ad_title"}).get_text().strip()

    return title

def get_offer_localization(soup):
    localization_name = soup.find('p', {"class": "css-7xdcwc-Text"})\
        .get_text().split(',')[0].strip()

    return localization_name

def get_offer_description(soup):
    description =  soup.find(class_='css-g5mtbi-Text').get_text().strip()
    
    return description

def get_offer_price(soup):
    price_txt = soup.find(class_="css-8kqr5l-Text").get_text()
    price = txt_to_float(price_txt)

    return price

def txt_to_float(text):
    """
    Parse number in text from olx offer to float
    """
    parsed = float("".join(text.replace(",",".").split(" ")[:-1]))

    return parsed

def get_offer_infos(soup, url_link):
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
        "url_link": url_link,
        "id": offer_id,
        "surface": offer_surface,
        "title": offer_title,
        "localization": offer_localization,
        "description": offer_descritpion,
        "price": offer_price
    }

    return details

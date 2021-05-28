from utils import txt_to_float

"""
Get content from otodom page
"""

def get_offer_id(soup):
    
    offer_id_desc = soup.find("div", {"class" : "css-jjerc6"})
    offer_id = int(offer_id_desc.text.split(" ")[-1]) if offer_id_desc else None

    return offer_id
    

def get_offer_surface(soup):

    surface_txt = soup.find("div", {"class" : "css-1ytkscc"})
    surface = txt_to_float(surface_txt.text) if surface_txt else None

    return surface

def get_offer_title(soup):

    title = soup.find("h1", {"class" : "css-46s0sq"})

    return title.text

def get_offer_localization(soup):

    localization_name = soup.find("a", {"class" : "css-1qz7z11"})
    localization_name = localization_name.text.split(",")[0].strip()

    return localization_name

def get_offer_description(soup):

    description =  soup.find("div", {"data-cy" : "adPageAdDescription"})
    
    return description.text

def get_offer_price(soup):

    price_txt = soup.find("strong", {"data-cy" : "adPageHeaderPrice"})

    price = txt_to_float(price_txt.text)

    return price

def get_offer_infos(soup, url_link):
    offer_id = get_offer_id(soup)
    offer_surface = get_offer_surface(soup)
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

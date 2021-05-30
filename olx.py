from utils import Utils

"""
Get content from olx page
"""

class OLXimporter:
    def __init__(self, soup, url_link):
        self.soup = soup
        self.url_link = url_link
        self.utils = Utils()

    def get_bottom_bar(self):
        bottom_bar = self.soup.find(class_="css-1v2fuie")

        return bottom_bar

    @staticmethod
    def get_offer_id(bottom_bar):
        offer_id = bottom_bar.find(class_="css-7oa68k-Text").get_text()
        
        return int(offer_id.split(' ')[-1])

    def get_details(self):
        offer_details = self.soup.find(class_="css-sfcl1s")

        return offer_details
    
    def get_offer_surface(self, details):
        details_items = details.find_all(class_="css-ox1ptj")
        surface_txt = details_items[-2].get_text().split(' ', 1)[-1]
        surface = self.utils.txt_to_float(surface_txt)

        return surface

    def get_offer_title(self):
        title = self.soup.find('h1', {"data-cy": "ad_title"}).get_text().strip()

        return title

    def get_offer_localization(self):
        localization_name = self.soup.find('p', {"class": "css-7xdcwc-Text"})\
            .get_text().split(',')[0].strip()

        return localization_name

    def get_offer_description(self):
        description =  self.soup.find(class_='css-g5mtbi-Text').get_text().strip()
        
        return description

    def get_offer_price(self):
        price_txt = self.soup.find(class_="css-8kqr5l-Text").get_text()
        price = self.utils.txt_to_float(price_txt)

        return price

    def get_offer_infos(self):
        bottom_bar = self.get_bottom_bar()
        details = self.get_details()
        """
        offer_id -> get from bottom bar
        offer_surfacet -> get from details at the top of page
        """
        offer_id = self.get_offer_id(bottom_bar)
        offer_surface = self.get_offer_surface(details)
        offer_title = self.get_offer_title()
        offer_localization = self.get_offer_localization()
        offer_descritpion = self.get_offer_description()
        offer_price = self.get_offer_price()

        details = {
            "url_link": self.url_link,
            "id": offer_id,
            "surface": offer_surface,
            "title": offer_title,
            "localization": offer_localization,
            "description": offer_descritpion,
            "price": offer_price,
        }

        return details

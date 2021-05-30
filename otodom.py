from utils import Utils
"""
Get content from otodom page
"""
class OTODOMimporter:
    def __init__(self, soup, url_link):
        self.soup = soup
        self.url_link = url_link
        self.utils = Utils()

    def get_offer_id(self):
        offer_id_desc = self.soup.find("div", {"class" : "css-jjerc6"})
        offer_id = int(offer_id_desc.text.split(" ")[-1]) if offer_id_desc else None

        return offer_id

    def get_offer_surface(self):
        surface_txt = self.soup.find("div", {"class" : "css-1ytkscc"})
        surface = self.utils.txt_to_float(surface_txt.text) if surface_txt else None

        return surface

    def get_offer_title(self):
        title = self.soup.find("h1", {"class" : "css-46s0sq"})

        return title.text

    def get_offer_localization(self):
        localization_name = self.soup.find("a", {"class" : "css-1qz7z11"})
        localization_name = localization_name.text.split(",")[0].strip()

        return localization_name

    def get_offer_description(self):
        description =  self.soup.find("div", {"data-cy" : "adPageAdDescription"})
        
        return description.text

    def get_offer_price(self):
        price_txt = self.soup.find("strong", {"data-cy" : "adPageHeaderPrice"})
        price = self.utils.txt_to_float(price_txt.text)

        return price

    def get_offer_infos(self):
        offer_id = self.get_offer_id()
        offer_surface = self.get_offer_surface()
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
            "price": offer_price
        }

        return details

from os import urandom

from otodom import OTODOMimporter
from olx import OLXimporter
from utils import Utils

import pandas as pd

BASE_URL = "https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/"

class Manage:
    def __init__(self, localization, surface_min, surface_max, seller):
        self.localization = localization
        self.surface_min = surface_min
        self.surface_max = surface_max
        self.seller = seller

        self.utils = Utils()
        self.olx_importer = OLXimporter()
        self.otodom_importer = OTODOMimporter()

    def scrap_olx(self):
        soup, url_link = self.utils.get_url_content(BASE_URL,
                                            page_number=None,
                                            localization=self.localization,
                                            surface_min=self.surface_min,
                                            surface_max=self.surface_max,
                                            seller=self.seller
                                            )

        num_of_pages = self.utils.get_page_count(soup)
        documents = list()

        for page_num in range(1, num_of_pages+1):
            soup, _ = self.utils.get_url_content(url_link=url_link, page_number=page_num)
            page_links = self.utils.get_page_links(soup=soup)

            for page_link in page_links:
                soup, _ = self.utils.get_url_content(page_link, None)
                is_olx = page_link.startswith('https://www.olx')

                if is_olx:
                    site_content = self.olx_importer.get_offer_infos(soup, url_link)
                else:
                    site_content = self.otodom_importer.get_offer_infos(soup, url_link)

                documents.append(site_content)

        df = pd.DataFrame().from_records(documents)

        df.to_excel('data.xlsx')

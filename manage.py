from os import urandom
import utils
import otodom
import olx

import pandas as pd


soup, url_link = utils.get_url_content("https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/", 
                page_number=None, 
                localization="opoczno",
                surface_min=0,
                surface_max=3000,
                seller="all"
                )

num_of_pages = utils.get_page_count(soup)
documents = list()

for page_num in range(1, num_of_pages+1):
    soup, _ = utils.get_url_content(url_link=url_link, 
                page_number=page_num, 
                surface_min=0,
                surface_max=3000,
                seller="")

    page_links = utils.get_page_links(soup=soup)

    for page_link in page_links:
        soup, _ = utils.get_url_content(page_link, None)
        is_olx = page_link.startswith('https://www.olx')
        
        if is_olx:
            site_content = olx.get_offer_infos(soup, url_link)
        else:
            site_content = otodom.get_offer_infos(soup, url_link)
        
        documents.append(site_content)

df = pd.DataFrame().from_records(documents)

df.to_excel('data.xlsx')
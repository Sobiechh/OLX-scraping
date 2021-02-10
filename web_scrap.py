import pandas as pd #dataframe
import requests #html request
from bs4 import BeautifulSoup #scrap page
import datetime as dt #to save file xslx


def scrap_OLX(loc, surface_min, surface_max, seller, media_on):
    dealers, surfaces, prices, descriptions, localizations, links, titles  = [], [], [], [], [], [], []#tables to dataframe

    #check surface min/max bug
    if surface_min>surface_max:
        return 'ŹLE PODANE WARTOŚCI\nPROSZĘ WPROWADZIĆ JESZCZE RAZ'

    page = requests.get(f'https://www.olx.pl/nieruchomosci/dzialki/{loc}/?search[filter_enum_type][0]=dzialki-budowlane&search%5Bfilter_float_m%3Afrom%5D={surface_min}&search%5Bfilter_float_m%3Ato%5D={surface_max}&search%5Bprivate_business%5D={seller}')
    soup = BeautifulSoup(page.content, 'html.parser')

    if soup.find_all(class_='emptynew large lheight18') != []:
        return 'BRAK WYNIKÓW W TEJ OKOLICY'

    num_of_sites = soup.find_all(class_ = 'block br3 brc8 large tdnone lheight24') #info about num of pages

    if num_of_sites == []:#if is empty means that there is one page
        num_of_sites=1
    else:
        num_of_sites = int(num_of_sites[-1].find('span').get_text()) # pare nums of pages to int (to loop)

    for i in range(1,num_of_sites+1): # [1,2,...., num of pages]
        page = requests.get(f'https://www.olx.pl/nieruchomosci/dzialki/{loc}/?search[filter_enum_type][0]=dzialki-budowlane&search%5Bfilter_float_m%3Afrom%5D={surface_min}&search%5Bfilter_float_m%3Ato%5D={surface_max}&search%5Bprivate_business%5D={seller}&page={i}')
        soup = BeautifulSoup(page.content, 'html.parser')

        offers = soup.find_all(class_ = 'offer-wrapper')

        offers_to_wrap_olx, offers_to_wrap_otodom = [],[]
        for offer in offers: #through offers
            for link in offer.find_all('a'): #through links
                sites = link.get('href') #get href value
                if sites != "#": #elims # dunno why this occurs
                    offers_to_wrap_olx.append(sites)#sites

        offers_to_wrap_otodom = [offer for offer in list(set(offers_to_wrap_olx)) if "otodom" in offer]
        offers_to_wrap_olx = [offer for offer in (list(set(offers_to_wrap_olx))) if "otodom" not in offer] #delete otodom from offers
        

        #OLX
        for offer in offers_to_wrap_olx:
            page = requests.get(offer)
            soup = BeautifulSoup(page.content, 'html.parser') #soup new page
            infos = soup.find_all(class_='offer-details__value') #get infos from tiles

            #deling promoted
            if offer[-9:] == ';promoted':
                links.append('del')
            else:
                links.append(offer)

            #tables to dataframe
            titles.append(soup.find(class_='offer-titlebox').find('h1').get_text().strip()) #add title


            dealers.append(infos[0].get_text().strip()) # private/buissness

            surfaces.append((''.join(infos[2].get_text().split(' ')[:-1]).strip())) #size of the surface

            prices.append(float(infos[3].get_text().split(' ')[0].strip())) #price/m^2
            
            #if main info contains word's like electricity', 'water', 'gas', 'media', 'armed' means that is medialised
            if any(med in soup.find(class_='clr lheight20 large').get_text() for med in ['prad','woda', 'gaz', 'media', 'uzbrojona']):
                descriptions.append('Tak')
            else:
                descriptions.append('Nie') # to del
            
            localizations.append(soup.find(class_='offer-user__address').p.get_text().split(',')[-1].strip()) # exact location
        
        #OTODOM
        # for offer in offers_to_wrap_otodom:
        #     page = requests.get(offer)
        #     soup = BeautifulSoup(page.content, 'html.parser') #soup new page

        #     if soup.find(class_='css-1ci0qpi') != None:
        #         infos = soup.find(class_='css-1ci0qpi').find_all('li') #infos under images
        #         surfaces.append(''.join(infos[0].find('strong').get_text().split()[:-1])) #surfaces
        #     else:
        #         surfaces.append('del')

        #     #link
        #     links.append(offer)

        #     titles.append(soup.find(class_='css-1ld8fwi').get_text()) #add title

        #     dealers.append(soup.find(class_='css-1gjwmw9').get_text().strip()) #add dealer

        #     if soup.find(class_='css-zdpt2t').get_text() == "":
        #         prices.append('del')
        #     else:
        #         prices.append(float(''.join(soup.find(class_='css-zdpt2t').get_text().split(' ')[:-1]))) #prices
            
        #     #medialize
        #     description = str(soup.find(class_='css-1bi3ib9').find_all('p')) #all description

        #     if any(med in description for med in ['prad','woda', 'gaz', 'media', 'uzbrojona']): #find if is medialized
        #         descriptions.append('Tak')
        #     else:
        #         descriptions.append('Nie') 
            
        #     localizations.append(soup.find(class_='css-12hd9gg').get_text().split('}')[-1]) #add localization


    #making df
    data_from_sites= pd.DataFrame({
        'Tytul':titles,
        'Oferta od': dealers,
        'Powierzchnia m^2': surfaces,
        'Cena za m^2': prices,
        'Media': descriptions,
        'Lokalizacja':localizations,
        'Link do strony':links
    })

    #elim duplicates
    data_from_sites = data_from_sites.drop_duplicates(subset='Link do strony')
    data_from_sites = data_from_sites.drop_duplicates(subset='Tytul')

    data_from_sites = data_from_sites.drop('Tytul', axis=1)

    #if we want to find plot with media
    if media_on == True: 
        data_from_sites = data_from_sites[data_from_sites['Media'] != 'Nie']
    else: #if we want to find plot without media
        data_from_sites = data_from_sites[data_from_sites['Media'] != 'Tak']

    #clearing some data
    data_from_sites = data_from_sites[data_from_sites['Link do strony'] != 'del']
    data_from_sites = data_from_sites[data_from_sites['Cena za m^2'] != 'del']

    prices = data_from_sites['Cena za m^2'].to_list() #we need this because we deleted rows with/without media se we need to calculate new averange prices

    now = dt.datetime.now() #datetime.now to .xslx file
    now = now.strftime("%d_%m_%Y Godzina %H_%M_%S") # : <- forbidden in file save
    data_from_sites.sort_values(by='Lokalizacja').to_excel(f'data/{loc}_{now}.xlsx')
    
    return f'{loc}\n SREDNIA CENA ZA DZIALKE {surface_min}-{surface_max} m^2\n  WYNOSI: {round(sum(prices)/len(prices),2)}zł/m^2' if len(prices)!=0 else f'BRAK WYNIKOW'

scrap_OLX('Lodz', 100, 25000, '', True)
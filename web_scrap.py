import re
import pandas as pd
import requests
from boto.support import regions
from bs4 import BeautifulSoup
import datetime as dt

#region
regions = ['Aleksandrow-Lodzki',
'Belchatow              ',
'Glowno                 ',
'Konstantynow-Lodzki    ', 
'Kutno                  ', 
'Lask                   ', 
'Leczyca                ', 
'Lodz                   ',
'Lowicz                 ', 
'Opoczno                ', 
'Ozorkow                ',
'Pabianice              ', 
'Piotrkow-Trybunalski   ', 
'Radomsko               ',
'Rawa-Mazowiecka        ', 
'Sieradz                ',
'Skierniewice           ', 
'Tomaszow-Mazowiecki    ', 
'Wielun                 ',
'Zdunska-Wola           ',    
'Zgierz                 ']

#localization
loc = 'Lodz'

#tables to dataframe
dealers, surfaces, prices, descriptions, localizations = [], [], [], [], []

#surface
surface_min= 1000
surface_max= 5000

#seller priv/company
temp = ['private','business']
seller = 'private'

page = requests.get(f'https://www.olx.pl/nieruchomosci/dzialki/{loc}/?search%5Bfilter_float_m%3Afrom%5D={surface_min}&search%5Bfilter_float_m%3Ato%5D={surface_max}&search%5Bprivate_business%5D={seller}')
soup = BeautifulSoup(page.content, 'html.parser')

num_of_sites = soup.find_all(class_ = 'block br3 brc8 large tdnone lheight24') #info about num of pages

if num_of_sites == []:#if is empty means that there is one page
    num_of_sites=1
else:
    num_of_sites = int(num_of_sites[-1].find('span').get_text()) # pare nums of pages to int (to loop)

for i in range(1,num_of_sites+1): # [1,2,...., num of pages]
    page = requests.get(f'https://www.olx.pl/nieruchomosci/dzialki/{loc}/?search%5Bfilter_float_m%3Afrom%5D={surface_min}&search%5Bfilter_float_m%3Ato%5D={surface_max}&search%5Bprivate_business%5D={seller}&page={i}')
    soup = BeautifulSoup(page.content, 'html.parser')

    offers = soup.find_all(class_ = 'offer-wrapper')

    offers_to_wrap = []

    for offer in offers: #through offers
        for link in offer.find_all('a'): #through links
            sites = link.get('href') #get href value
            if sites != "#": #elims # dunno why this occurs
                offers_to_wrap.append(sites)#sites

    offers_to_wrap = [offer for offer in (list(set(offers_to_wrap))) if "otodom" not in offer] #delete otodom from offers

    for offer in offers_to_wrap:
        page = requests.get(offer)
        soup = BeautifulSoup(page.content, 'html.parser') #soup new page
        infos = soup.find_all(class_='offer-details__value') #get infos from tiles

        #tables to dataframe
        dealers.append(infos[0].get_text().strip()) # private/buissness

        surfaces.append(float(''.join(infos[2].get_text().split(' ')[:2]).strip())) #size of the surface

        prices.append(float(infos[3].get_text().split(' ')[0].strip())) #price/m^2
        
        #if main info contains word's like electricity', 'water', 'gas', 'media', 'armed' means that is medialised
        if any(med in soup.find(class_='clr lheight20 large').get_text() for med in ['prad','woda', 'gaz', 'media', 'uzbrojona']):
            descriptions.append('Tak')
        else: #if not append no
            descriptions.append('Nie')
        
        localizations.append(soup.find(class_='offer-user__address').p.get_text().split(',')[-1].strip()) # exact location

print(f'TO WSZYSTKO Z {loc} SREDNIA CENA ZA DZIALKE {surface_min}-{surface_max} m^2 TO: {round(sum(prices)/len(prices),2)}zł/m^2')

#making df
data_from_sites= pd.DataFrame({
    'Oferta od': dealers,
    'Powierzchnia m^2': surfaces,
    'Cena za m^2': prices,
    'Media': descriptions,
    'Lokalizacja':localizations
})

#tests

now = dt.datetime.now() #datetime now to .xslx file
now = now.strftime("Dane Data %d_%m_%Y Godzina %H_%M_%S") # : <- forbidden in file save
data_from_sites.sort_values(by='Lokalizacja').to_excel(f'data/{loc}_{now}.xlsx')
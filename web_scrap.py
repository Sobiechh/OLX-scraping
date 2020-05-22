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

#surface
surface_min= 20
surface_max= 400

#seller priv/company
temp = ['private','business']
seller = temp[0]

for i in range(1):
    #page 
    page = requests.get(f'https://www.olx.pl/nieruchomosci/dzialki/{regions[7].strip()}/?search%5Bfilter_float_m%3Afrom%5D={surface_min}&search%5Bfilter_float_m%3Ato%5D={surface_max}&search%5Bprivate_business%5D={seller}')
    soup = BeautifulSoup(page.content, 'html.parser')

    offers = soup.find_all(class_ = 'offer-wrapper')

    offers_to_wrap = []

    for offer in offers: #through offers
        for link in offer.find_all('a'): #through links
            sites = link.get('href') #get href value
            if sites != "#": #elims # dunno why this occurs
                offers_to_wrap.append(sites)
        #print(f"{offer.find(class_='lheight22 margintop5').get_text().strip()}  - {offer.find(class_='price').get_text()}")

    offers_to_wrap = [offer for offer in (list(set(offers_to_wrap))) if "otodom" not in offer] #delete otodom from offers


    dealers, surfaces, prices, descriptions, localizations = [], [], [], [], []
    for offer in offers_to_wrap:
        page = requests.get(offer)
        soup = BeautifulSoup(page.content, 'html.parser') #soup new page
        infos = soup.find_all(class_='offer-details__value') #get infos from tiles

        #tables to dataframe

        info_price = soup.find(class_='pricelabel').get_text().strip()
#         print(f"tytul: {soup.find(class_='offer-titlebox').h1.get_text().strip()}\n\
# cena: {info_price[:-13].strip() if 'negocjacji' in info_price else info_price.strip()}\n\
# od kogo: {infos[0].get_text().strip()}\n\
# powierzchnia: {infos[2].get_text().strip()}\n\
# cena za m^2: {infos[3].get_text().strip()}\n\
# lokalizacja: {soup.find(class_='offer-user__address').p.get_text().split(',')[-1].strip()}\
# ")
        dealers.append(infos[0].get_text().strip()) # private/buissness
        surfaces.append(infos[2].get_text().split(' ')[0].strip()) #size of the surface
        prices.append(float(infos[3].get_text().split(' ')[0].strip())) #price/m^2
        
        #if main info contains word's like electricity', 'water', 'gas', 'media', 'armed' means that is medialised
        if any(med in soup.find(class_='clr lheight20 large').get_text() for med in ['prad','woda', 'gaz', 'media', 'uzbrojona']):
            descriptions.append('Tak')
        else: #if not append no
            descriptions.append('Nie')
        
        localizations.append(soup.find(class_='offer-user__address').p.get_text().split(',')[-1].strip()) # exact location

    print(f'TO WSZYSTKO Z {regions[7].strip()} SREDNIA CENA TO: {round(sum(prices)/len(prices),2)}')


#making df
data_from_sites= pd.DataFrame({
    'Oferta od': dealers,
    'Powierzchnia m^2': surfaces,
    'Cena za m^2': prices,
    'Media': descriptions,
    'Lokalizacja':localizations
})

print(data_from_sites.head())

now = dt.datetime.now()
now = now.strftime("Dane Data %d_%m_%Y Godzina %H_%M_%S")

data_from_sites.to_csv(f'{now}.csv')


#print(week)
#items = week.find_all(class_ = 'tombstone-container') #class_ <- bc 'class' is rereved
#print(items[0].find(class_='period-name').get_text()) #biore items 0, czyli te opcje z today, potem biore klase w ktorej zapisane jest wlasnie dzien,
# i wyswietlam nazwe tego dnai, bez get_text() wyswietli mi caly paragraf

#print(items)

# period_names=[item.find(class_='period-name').get_text() for item in items]
# short_descriptions=[item.find(class_='short-desc').get_text() for item in items]
# temps=[item.find(class_='temp').get_text() for item in items]


# weather_stuff= pd.DataFrame({
#     'period': period_names,
#     'description': short_descriptions,
#     'temperature': temps
# })
#
# print(weather_stuff)
#
# weather_stuff.to_csv('weather.csv')
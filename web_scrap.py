import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

#page 
page = requests.get('https://www.olx.pl/nieruchomosci/dzialki/lodzkie/')
soup = BeautifulSoup(page.content, 'html.parser')

offers = soup.find_all(class_ = 'offer-wrapper')

offers_to_wrap = []

for offer in offers: #through offers
    for link in offer.find_all('a'): #through links
        sites = link.get('href') 
        if sites != "#": #elims # dunno why this occurs
            offers_to_wrap.append(sites)
    #print(f"{offer.find(class_='lheight22 margintop5').get_text().strip()}  - {offer.find(class_='price').get_text()}")

offers_to_wrap = [offer for offer in (list(set(offers_to_wrap))) if "otodom" not in offer] #delet otodom from offers

for offer in offers_to_wrap:
    print(offer)



#print(week)
#items = week.find_all(class_ = 'tombstone-container') #class_ <- bc 'class' is rereved
#print(items[0].find(class_='period-name').get_text()) #biore items 0, czyli te opcje z today, potem biore klase w ktorej zapisane jest wlasnie dzien,
# i wyswietlam nazwe tego dnai, bez get_text() wyswietli mi caly paragraf

#print(items)

# period_names=[item.find(class_='period-name').get_text() for item in items]
# short_descriptions=[item.find(class_='short-desc').get_text() for item in items]
# temps=[item.find(class_='temp').get_text() for item in items]

# print(period_names)
# print(short_descriptions)
# print(temps)
#
# weather_stuff= pd.DataFrame({
#     'period': period_names,
#     'description': short_descriptions,
#     'temperature': temps
# })
#
# print(weather_stuff)
#
# weather_stuff.to_csv('weather.csv')
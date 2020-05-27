import requests #html request
from bs4 import BeautifulSoup #scrap page

# page = requests.get('https://www.otodom.pl/oferta/urokliwa-dzialka-w-prestizowej-okolicy-ID45KFK.html?')
# soup = BeautifulSoup(page.content, 'html.parser') #soup new pa
# # surface,price/m^2,med,loc,link
#print(soup.find(class_='css-1gjwmw9').get_text().strip()) #add dealer

# infos = soup.find(class_='css-1ci0qpi').find_all('li')

# print(''.join(infos[0].find('strong').get_text().split()[:-1])) #add dealer


#print(''.join(soup.find(class_='css-zdpt2t').get_text().split(' ')[:-1]))

# description = str(soup.find(class_='css-1bi3ib9').find_all('p'))

# if any(med in description for med in ['prad','woda', 'gaz', 'media', 'uzbrojona']):
#     print('Tak')


#print(soup.find(class_='css-12hd9gg').get_text().split('}')[-1])

page = requests.get(f'https://www.olx.pl/oferta/sprzedam-dzialke-budowlana-ul-rataja-CID3-IDET3Np.html#ddbee2a1ec')
soup = BeautifulSoup(page.content, 'html.parser')

titlebox = soup.find(class_='offer-titlebox')
print(soup.find(class_='offer-titlebox').find('h1').get_text().strip())
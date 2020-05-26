import requests #html request
from bs4 import BeautifulSoup #scrap page

page = requests.get('https://www.otodom.pl/oferta/pieknie-polozone-dzialki-okolice-kalonki-ID44nGS.html#399ef518c8')
soup = BeautifulSoup(page.content, 'html.parser') #soup new pa
# surface,price/m^2,med,loc,link
#print(soup.find(class_='css-1gjwmw9').get_text().strip()) #add dealer

# infos = soup.find(class_='css-1ci0qpi').find_all('li')

# print(''.join(infos[0].find('strong').get_text().split()[:-1])) #add dealer


print(''.join(soup.find(class_='css-zdpt2t').get_text().split(' ')[:-1]))
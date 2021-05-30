from selenium import webdriver

driver = webdriver.Chrome()

driver.get('https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/Lodz/?search%5Bfilter_float_m%3Afrom%5D=5000&search%5Bfilter_float_m%3Ato%5D=8000&')
page_source = driver.page_source

print(page_source)
import requests
from bs4 import BeautifulSoup
from lxml import etree

def todos_productos(filt_data):
    l_title = []
    l_descrip = []
    l_address = []
    l_surface = []
    l_price = []
    siguiente = f'https://inmuebles.mercadolibre.com.ar'
    for k in filt_data:
        siguiente = f'{siguiente}/{filt_data[k]}'
    while True:
        r = requests.get(siguiente)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            #Titulos
            titles = soup.find_all("h2", attrs={"class": "ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title"})
            titles = [t.text for t in titles]
            l_title.extend(titles)
            # Descripción
            short_des = soup.find_all("a", {"class": "ui-search-result__content ui-search-link"})#"price-tag-text-sr-only"})#"price-t
            short_des = [sd.text for sd in short_des]
            l_descrip.extend(short_des)
            # Dirección
            dom = etree.HTML(str(soup))
            address = dom.xpath('//li[@class="ui-search-layout__item"]/div/div/a[@class="ui-search-result__content ui-search-link"]//div//div//span[@class="ui-search-item__group__element ui-search-item__location shops__items-group-details"]')
            address = [a.text for a in address]
            l_address.extend(address)
            # Superficie
            surfcover_room = soup.find_all("ul", {"class": "ui-search-card-attributes ui-search-item__group__element shops__items-group-details"})
            surfcover_room = [sr.text for sr in surfcover_room]
            l_surface.extend(surfcover_room)
            # Precios
            dom = etree.HTML(str(soup))
            price = dom.xpath('//li[@class="ui-search-layout__item"]//span[@class="price-tag-text-sr-only"]')
            price = [p.text for p in price]
            l_price.extend(price)
            
            # Validación de la ppaginación
            ini = soup.find_all("span", attrs={"class": "andes-pagination__link"})[0].text
            ini = int(ini)
            tot = soup.find_all("li", attrs={"class": "andes-pagination__page-count"})[0].text.split()[1]
            tot = int(tot)     
        else:
            break
        print(ini, tot)
        if ini == tot:
            break
        siguiente = dom.xpath('//div[@class="ui-search-pagination shops__pagination-content"]/ul/li[contains(@class,"--next")]/a')[0].get('href')

    return l_title, l_descrip, l_address, l_surface, l_price

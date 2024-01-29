import threading
from selenium import webdriver
from bs4 import BeautifulSoup
import itertools
import time
import sys
import re
import json
import requests

allProducts = []

def amazon(term):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import itertools
    import time

    # Load the Costco product page
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.com/s?k=" + term)

    # Wait for the JavaScript to finish loading
    time.sleep(10)

    # Extract the HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    name = []
    price = []
    pricedec = []
    weight = []
    link= []
    image = []
    product_links = []
    productlinks = []
    # Find the desired elements and extract their text

    price = [p.getText(strip=True) for p in soup.find_all("span", class_="a-price-whole")]
    #for price_elm in soup.find_all("span", class_="a-price-whole"):
        #price.append(price_elm.get_text(strip=True))

    pricedec = [p.getText(strip=True) for p in soup.find_all("span", class_="a-price-fraction")]
    #for pricedec_elm in soup.find_all("span", class_="a-price-fraction"):
        #pricedec.append(pricedec_elm.get_text(strip=True))

    name = [p.getText(strip=True) for p in soup.find_all("span", {"class": "a-size-base-plus a-color-base a-text-normal"})]
    #for product_elm in soup.find_all("span", {"class": "a-size-base-plus a-color-base a-text-normal"}):
        #name.append(product_elm.get_text(strip=True))

    #Webscrapes Product Links
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/sspa/') and not href.endswith('customerReviews'):
            product_links.append('https://www.amazon.com' + href)

    #Deletes the duplicates in the product links
    for i in product_links:
        if i not in productlinks:
            productlinks.append(i)

    #image = [not p['src'].endswith('SS200_.png') for p in soup.find_all("span", {"class": "a-size-base-plus a-color-base a-text-normal"})]
    for image_elm in soup.find_all('img'):
        if not image_elm['src'].endswith('SS200_.png'):
            image.append(image_elm['src'])

    #Deletes the first several images that appear
    del(image[0])
    del(image[0])
    del(image[0])
    del(image[0])
    del(image[0])
    del(image[0])

    #Combines all the information in a printable format
    # Close the web driver
    for i in range(len(name)):
        product = {
            'store': "amazon",
            'name': name[i],
            'price': float(re.sub(",", "", "" + price[i] + "." + pricedec[i])),
            'image': image[i],
            'link': productlinks[i]
        }
        allProducts.append(product)

    # Close the web driver
    driver.quit()

def costco(term):
    # Load the Costco product page
    driver = webdriver.Chrome()
    driver.get("https://www.costco.com/CatalogSearch?keyword=" + term + "&deliveryFacetFlag=true&sortBy=item_location_pricing_salePrice+asc")

    # Wait for the JavaScript to finish loading

    # Extract the HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    price = [p.getText(strip=True)[1:] for p in soup.find_all("div", {"class": "price"})]
   
    name = [p.getText(strip=True) for p in soup.find_all("span",{"class": "description"})]

    image = [p.find('img').get('src') for p in soup.find_all('a', class_="product-image-url")]

    link = [p['href'] for p in soup.find_all('a', class_="product-image-url")]

    for i in range(len(name)):
        product = {
            'store': "costco",
            'name': name[i],
            'price': float(re.sub(",", "", price[i])),
            'image': image[i],
            'link': link[i]
        }
        allProducts.append(product)
    driver.quit()

#kroger api
def kroger(terms, zipCode):
    from python_kroger_client.client import (
        KrogerServiceClient,
    )

    from python_kroger_client.config import (
        encoded_client_token,
    )

    service_client = KrogerServiceClient(encoded_client_token=encoded_client_token)
    locations = service_client.get_locations(zipCode, within_miles=10, limit=10)
    items= service_client.search_products(term=terms, limit=10, location_id=locations[1].id)

    #to make a hyper link it is "https://www.kroger.com/search?query=" + products[1].Id + "&searchType=default_search" image is .image
    for i in range(len(items)):
        product = {
            'store': "kroger",
            'name': items[i].getDescription(),
            'image': items[i].getImage(),
            'link': "https://www.kroger.com/search?query=" + items[i].getID() + "&searchType=default_search" 
        }
        allProducts.append(product)

def samsClub(term):
    url = "https://www.samsclub.com/s/" + term

    binger = requests.get(url).text

    soup = BeautifulSoup(binger, 'html5lib')

    #Code that finds all the name's of the products and prints them
    names = [p.getText(strip=True) for p in soup.find_all("div", class_="sc-pc-title-medium")]

    #Code that finds all the price's of the products and prints them
    #product_prices = [p["title"].split()[-1] for p in soup.find_all("span", title_="Price-group")]

    price = [p['title'].split(" ")[2] for p in soup.find_all("span", class_="Price-group")]

    link = [p['href'] for p in soup.find_all('a', class_="bst-link bst-link-small bst-link-primary sc-pc-medium-desktop-card-canary-product-link")]

    image = [p['src'] for p in soup.find_all('img', class_="sc-pc-image-controller sc-image-wrapper-full-res sc-image-wrapper-full-res-loaded")]
   
    for i in range(len(names)):
        product = {
            'store': "samsClub",
            'name': names[i],
            'price': float(price[i][1:]),
            'image': image[i],
            'link': "https://www.samsclub.com" + link[i]
        }
        allProducts.append(product)      

def traderJoes(term):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import itertools
    import time
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.by import By

    # Load the Costco product page
    driver = webdriver.Chrome()
    driver.get("https://www.traderjoes.com/home/search?q=" + term + "&section=products&global=yes")
    
    # Wait for the JavaScript to finish loading

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Click on the button

    name = []
    price = []
    weight = []
    image = []
    link = []
    # Find the desired elements and extract their text

    price = [p.getText(strip=True)[1:] for p in soup.find_all("span", {"class": "ProductPrice_productPrice__price__3-50j"})]
    #for price_elm in soup.find_all("span", {"class": "ProductPrice_productPrice__price__3-50j"}):
        #price.append(price_elm.get_text(strip=True))

    weight = [p.getText(strip=True) for p in soup.find_all("span", {"class": "ProductPrice_productPrice__unit__2jvkA"})]
    #for weight_elm in soup.find_all("span", {"class": "ProductPrice_productPrice__unit__2jvkA"}):
        #weight.append(weight_elm.get_text(strip=True))

    name = [p.getText(strip=True) for p in soup.find_all("a", {"class": "Link_link__1AZfr SearchResultCard_searchResultCard__titleLink__2nz6x"})]
    #for product_elm in soup.find_all("a", {"class": "Link_link__1AZfr SearchResultCard_searchResultCard__titleLink__2nz6x"}):
        #name.append(product_elm.get_text(strip=True))

    link = [p.get("href") for p in soup.find_all("a", {"class": "Link_link__1AZfr SearchResultCard_searchResultCard__titleLink__2nz6x"})]
    #for link_elm in soup.find_all("a", {"class": "Link_link__1AZfr SearchResultCard_searchResultCard__titleLink__2nz6x"}):
        #link_elm = "https://www.traderjoes.com" + link_elm.get("href")
        #link.append(link_elm)

    image = [p['src'] for p in soup.find_all('img')]
    #for image_elm in soup.find_all('img'):
        #image.append(image_elm['src'])

    for i in range(len(name)):
            product = {
            'store': "trader Joes",
            'name': name[i],
            'price':float(re.sub(",", "", price[i])),
            'image': image[i],
            'link':"https://www.traderjoes.com" + link[i]
            }
            allProducts.append(product)

    # Close the web driver
    driver.quit()
def ebay(term):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import itertools
    import time

    # Load the Costco product page
    driver = webdriver.Chrome()
    driver.get("https://www.ebay.com/sch/i.html?_nkw=" + term)

    time.sleep(10)
    # Extract the HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    name = []
    price = []
    image = []
    images = []
    product_links = []
    productlinks = []
    # Find the desired elements and extract their text

    price = [p.getText(strip=True)[1:][:4] for p in soup.find_all("span", class_="s-item__price")]

    name =  [p.getText(strip=True) for p in soup.find_all("span", {"role": "heading"})]

    image = [p['src'] for p in soup.find_all('img')]
    #Webscrapping image links

    images_elm = []
    for i in range (len(image)):
        if image[i].startswith('https://i.ebayimg.com/thumbs'):
            images_elm.append(image[i])

    for i in range (len(images_elm)):
        if images_elm[i] not in images:
            images.append(images_elm[i])

    #Webscrapes Product Links
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        product_links.append(href)

    #Sorting Product Links
    productlinks_elm = []
    for i in range(len(product_links)):
        if product_links[i].startswith('https://www.ebay.com/itm/'):
            if i not in productlinks_elm:           
                productlinks_elm.append(product_links[i])

    for i in range(len(productlinks_elm)):
        if i%2 == 0:
            productlinks.append(productlinks_elm[i])

    del(name[0])
    for i in range(len(name)):
            product = {
            'store': "Ebay",
            'name': name[i],
            'price': float(re.sub(",", "", price[i])),
            'image': image[i],
            'link':productlinks[i]
            }
            allProducts.append(product)
    # Close the web driver
    driver.quit()

def etsy(term):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import itertools
    import time

    # Load the Costco product page
    driver = webdriver.Chrome()
    driver.get("https://www.etsy.com/search?q="+ term + "&ref=search_bar")

    # Wait for the JavaScript to finish loading


    # Extract the HTML content
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    product = []
    price = []
    image = []
    product_links = []
    # Find the desired elements and extract their text


    price = [p.getText(strip=True) for p in soup.find_all("span", class_="currency-value")]

    name = [p.getText(strip=True) for p in soup.find_all("h3", {"class": "wt-text-caption v2-listing-card__title wt-text-truncate"})]
    
    image = [p['src'] for p in soup.find_all('img')]

    #Webscrapes Product Links
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('https') and not href.startswith('/c/'):
            product_links.append(href)

    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])
    del(product_links[0])

    for i in range(len(name)):
        product = {
        'store': "Etsy",
        'name': name[i],
        'price':float(re.sub(",", "", price[i])),
        'image': image[i],
        'link':product_links[i]
        }
        allProducts.append(product)

    # Close the web driver
    driver.quit()
term = "laptop" #sys.argv[1]
zipCode = 37027 #sys.argv[2]

if __name__ == '__main__':
    #amazonThread = Process(target = amazon, args=(term,))
    costcoThread = threading.Thread(target = costco, args=(term,))
    ebayThread = threading.Thread(target = ebay, args = (term,))
    etsyThread = threading.Thread(target = etsy, args = (term,))
    krogerThread = threading.Thread(target = kroger, args = (term, zipCode,))
    samsClubThread = threading.Thread(target = samsClub, args = (term,))
    traderJoesThread = threading.Thread(target= traderJoes, args=(term,))

    #amazonThread.start()
    costcoThread.start()
    ebayThread.start()
    etsyThread.start()
    krogerThread.start()
    samsClubThread.start()
    traderJoesThread.start()

    #amazonThread.join()
    costcoThread.join()
    ebayThread.join()
    etsyThread.join()
    krogerThread.join()
    samsClubThread.join()
    traderJoesThread.join()
    
    
    allProducts = sorted(allProducts, key=lambda d: d['price'])

    print(allProducts)
    sys.stdout.flush()
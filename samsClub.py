from bs4 import BeautifulSoup
import requests
import itertools
from selenium import webdriver

url = "https://www.samsclub.com/b/fruit-nuts/2259?xid=cat-_headerGrid_0_10"
#will turn all of this into a for loop that runs through all the links

binger = requests.get(url).text

soup = BeautifulSoup(binger, 'html5lib')
print(soup.prettify())

#Code that helps you find a specific item in the code
results = binger.find('doritos')

print(results)          

price = binger.find("4.48")

print(price)

#Code that finds all the name's of the products and prints them
product_names = [p.getText(strip=True) for p in soup.find_all("div", class_="sc-pc-title-medium")]

print(product_names)

#Code that finds all the price's of the products and prints them
product_prices = [p["title"].split()[-1] for p in soup.find_all("span", title_="Price-group")]

print(product_prices)

pproduce_prices = [p["title"].split()[-1] for p in soup.find_all("span", class_="Price-group")]

print(pproduce_prices)

#Code that combines the names and the prices together in one list
results = {k: v for k, v in itertools.zip_longest(product_names, pproduce_prices, fillvalue="N/A")}

for product, price in results.items():
    print(product, price)                

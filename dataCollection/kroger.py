import sys
from python_kroger_client.client import (
    KrogerServiceClient,
)

from python_kroger_client.config import (
    encoded_client_token,
)

def add_to_items(items, product, quantity):
    """ Adds specified item to list of items with given quantity and returns items

    Arguments:
        items {array} -- An array of items to purchase
        product {Product} -- The product we want to buy
        quantity {int} -- How much of the product we want to buy
    """
    item_to_add = {
        "upc": product.upc,
        "quantity": quantity
    }
    items.append(item_to_add)
    return items



service_client = KrogerServiceClient(encoded_client_token=encoded_client_token)
locations = service_client.get_locations("zipcode", within_miles=10, limit=10)
products = service_client.search_products(term="ham", limit=10, location_id=locations[1].id)

#to make a hyper link it is "https://www.kroger.com/search?query=" + products[1].Id + "&searchType=default_search" image is .image
print(products)
sys.stdout.flush()
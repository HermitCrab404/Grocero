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
locations = service_client.get_locations(sys.argv[2], within_miles=10, limit=10)
products = service_client.search_products(term=sys.argv[1], limit=10, location_id=locations[1].id)

for p in products: print(p)

for l in locations: print(l)

print(products)
sys.stdout.flush()
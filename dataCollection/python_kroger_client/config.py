import base64
import os

# Get these 3 values from registering your developer account/application with https://developer.kroger.com/
client_id = "grocero-03ca19d4efc60e7ff635d612f8e401963976485596336484316"
client_secret = "qAMxV2sjxWAOVI8ypdu2zCHDngfn15ionBTBcD03"
redirect_uri = "http://localhost:8888"

# Authentication requires base64 encoded id:secret, which is precalculated here
encoded_client_token = base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode('ascii')

# This is here to make testing the customer client easier.  Obviously we would never want to ask a user for 
# this information.
# FUTURE: Remove this in favor of using the standard authorization path
customer_username = 'grocerooffical@gmail.com'
customer_password = '@Grocero24_'

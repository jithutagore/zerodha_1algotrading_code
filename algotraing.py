import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

api_key = "your_api_key"
api_secret = "your_api_secret"
access_token = "your_access_token"
kite = KiteConnect(api_key=api_key)

# Set access token
kite.set_access_token(access_token)

# Place order
order_id = kite.place_order(variety="regular",
                             exchange="NSE",
                             tradingsymbol="RELIANCE",
                             transaction_type="BUY",
                             quantity=100,
                             order_type="MARKET",
                             product="CNC",
                             validity="DAY")
print("Order placed. ID is:", order_id)

"""
Zerodha is an Indian stock brokerage firm that offers a number of trading
 platforms and tools, including an application programming interface (API) that allows 
 developers to connect to Zerodha's trading systems and build custom trading strategies. 
 To use Zerodha's API, you will first need to create an account with Zerodha and generate
  an API key.

Once you have your API key, you can use Python to build and execute trading 
strategies. Here is a sample code that uses Zerodha's API to place a buy order 
for 100 shares of Reliance Industries:

In this example, we first import the necessary libraries and set up a 
KiteConnect object with our API key. We then set the access token to connect to 
Zerodha's servers, which allows us to place orders.

We use the place_order method of the KiteConnect object to place a buy order for
 100 shares of Reliance Industries on the National Stock Exchange (NSE). We specify 
 the order type as "MARKET", which means the order will be executed at the current 
 market price. We also set the product type to "CNC", which means the shares will be 
 held in our account as delivery holdings.

Finally, we print the order ID to confirm that the order was successfully placed.

Note that this is just a simple example to illustrate the basic process of placing 
an order using Zerodha's API. To build a more complex trading strategy, you will need 
to combine this code with other Python libraries and code to analyze market data, make 
trading decisions, and execute orders.


"""
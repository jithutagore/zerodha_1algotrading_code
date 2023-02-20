import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import numpy as np

logging.basicConfig(level=logging.DEBUG)

api_key = "your_api_key"
api_secret = "your_api_secret"
access_token = "your_access_token"
kite = KiteConnect(api_key=api_key)

# Set access token
kite.set_access_token(access_token)

# Set up streaming data connection
symbol = "RELIANCE"
tickers = [symbol]
kws = KiteTicker(api_key, access_token)
last_price = []

def on_ticks(ws, ticks):
    for tick in ticks:
        last_price.append(tick['last_price'])

def on_connect(ws, response):
    ws.subscribe(tickers)
    ws.set_mode(ws.MODE_FULL, tickers)

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()

# Implement trading strategy
def calculate_ma(window):
    return np.mean(last_price[-window:])

while True:
    ma_short = calculate_ma(10)  # Short-term moving average
    ma_long = calculate_ma(50)  # Long-term moving average
    if ma_short > ma_long:
        # Place buy order
        order_id = kite.place_order(variety="regular",
                                     exchange="NSE",
                                     tradingsymbol=symbol,
                                     transaction_type="BUY",
                                     quantity=100,
                                     order_type="MARKET",
                                     product="CNC",
                                     validity="DAY")
        print("Buy order placed. ID is:", order_id)
    elif ma_short < ma_long:
        # Place sell order
        order_id = kite.place_order(variety="regular",
                                     exchange="NSE",
                                     tradingsymbol=symbol,
                                     transaction_type="SELL",
                                     quantity=100,
                                     order_type="MARKET",
                                     product="CNC",
                                     validity="DAY")
        print("Sell order placed. ID is:", order_id)

"""
 moving average is a commonly used technical indicator in algo trading strategies.
  Here is a sample code that uses moving averages to implement a simple trading strategy:
  In this example, we first set up a KiteConnect object and connect to Zerodha's API using our API key and access token.
   We then set up a streaming data connection for a single symbol using the KiteTicker library.

We define a callback function on_ticks that receives market data updates and appends the latest price to a list last_price. 
We also define a callback function on_connect that subscribes to the symbol and sets the streaming mode to MODE_FULL.

We then implement our trading strategy in a loop. We use the calculate_ma function to calculate the short-term and long-term 
moving averages of the last n prices, where n is the window size. In this example, we use a window size of 10 for the short-term 
moving average and 50 for the long-term moving average.

We then compare the short-term and long-term moving averages and place a buy order for 100 shares if the short-term moving average 
is above the long-term moving average, and a sell order for 100 shares if the short-term moving average is below the long-term moving 
average.

Note that this is just a simple example to illustrate the basic process of implementing a trading strategy based on moving averages.
 To build a more complex strategy, you will need to combine this code with other Python libraries and code to analyze market data, 
 make trading decisions, and execute orders.
"""
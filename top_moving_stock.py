import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

api_key = "your_api_key"
api_secret = "your_api_secret"
access_token = "your_access_token"
kite = KiteConnect(api_key=api_key)

# Set access token
kite.set_access_token(access_token)

# Set up streaming data connection
symbols = ["INFY", "TCS", "HDFCBANK", "ICICIBANK", "RELIANCE"]
tickers = [kite.EXCHANGE_NSE + ":" + symbol for symbol in symbols]
kws = KiteTicker(api_key, access_token)
ltp = {}

def on_ticks(ws, ticks):
    for tick in ticks:
        ltp[tick['instrument_token']] = tick['last_price']

def on_connect(ws, response):
    ws.subscribe(tickers)
    ws.set_mode(ws.MODE_FULL, tickers)

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()

# Wait for data to accumulate
while len(ltp) < len(tickers):
    pass

# Calculate daily percentage change
df = pd.DataFrame(ltp.items(), columns=['instrument_token', 'ltp'])
df['symbol'] = df['instrument_token'].apply(lambda x: x.split(":")[1])
df['prev_close'] = df['symbol'].apply(lambda x: kite.ltp(kite.EXCHANGE_NSE + ":" + x)['ohlc']['close'])
df['pct_change'] = (df['ltp'] - df['prev_close']) / df['prev_close'] * 100

# Find top movers
top_movers = df.nlargest(5, 'pct_change')
print(top_movers)

"""
In this example, we first set up a KiteConnect object and connect to Zerodha's API 
using our API key and access token. We then set up a streaming data connection for a 
list of symbols using the KiteTicker library.

We define a callback function on_ticks that receives market data updates and updates 
the latest price for each symbol in a dictionary ltp. We also define a callback function
 on_connect that subscribes to the symbols and sets the streaming mode to MODE_FULL.

We then wait for the ltp dictionary to accumulate the latest price for all the symbols.

We use the ltp dictionary to create a pandas DataFrame and calculate the daily
 percentage change for each symbol based on the previous day's closing price. We then 
 use the nlargest method to find the top 5 movers based on their percentage change.

Note that this is just a simple example to illustrate the basic process of 
finding top movers based on their daily percentage change. To build a more complex 
trading strategy, you will need to combine this code with other Python libraries and 
code to analyze market data, make trading decisions, and execute orders.




Regenerate
"""
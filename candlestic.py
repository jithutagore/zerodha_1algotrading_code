import logging
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import talib
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

api_key = "your_api_key"
api_secret = "your_api_secret"
access_token = "your_access_token"
kite = KiteConnect(api_key=api_key)

# Set access token
kite.set_access_token(access_token)

# Set up streaming data connection
symbol = "INFY"
ticker = kite.EXCHANGE_NSE + ":" + symbol
kws = KiteTicker(api_key, access_token)
candles = {}

def on_ticks(ws, ticks):
    for tick in ticks:
        if tick['instrument_token'] not in candles:
            candles[tick['instrument_token']] = []

        candles[tick['instrument_token']].append(tick)

def on_connect(ws, response):
    ws.subscribe([ticker])
    ws.set_mode(ws.MODE_FULL, [ticker])

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()

# Wait for data to accumulate
while len(candles) == 0:
    pass

# Convert ticks to pandas DataFrame
df = pd.DataFrame(candles[tick['instrument_token']])
df = df[['date', 'open', 'high', 'low', 'close']]

# Calculate candlestick patterns
patterns = talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])
df['pattern'] = patterns

# Find trading opportunities
if df['pattern'].iloc[-1] == 101:
    kite.place_order(
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol=symbol,
        quantity=1,
        transaction_type=kite.TRANSACTION_TYPE_BUY,
        order_type=kite.ORDER_TYPE_MARKET,
        product=kite.PRODUCT_MIS,
        variety=kite.VARIETY_REGULAR
    )
elif df['pattern'].iloc[-1] == -101:
    kite.place_order(
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol=symbol,
        quantity=1,
        transaction_type=kite.TRANSACTION_TYPE_SELL,
        order_type=kite.ORDER_TYPE_MARKET,
        product=kite.PRODUCT_MIS,
        variety=kite.VARIETY_REGULAR
    )

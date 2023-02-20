import numpy as np
import talib
import time
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException

# Enter your API credentials here
api_key = 'your_api_key'
api_secret = 'your_api_secret'
access_token = 'your_access_token'

# Initialize KiteConnect client
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Define parameters for historical data retrieval
instrument_token = 256265  # NSE stock token
interval = 'minute'  # Time interval for historical data (minute, day, week, etc.)
from_date = '2022-02-01'
to_date = '2022-02-17'

# Retrieve historical price data using KiteConnect
historical_data = kite.historical_data(instrument_token, from_date, to_date, interval)

# Convert the data to a pandas DataFrame
data = pd.DataFrame(historical_data)

# Calculate the 20-day moving average
data['ma20'] = talib.SMA(data['close'], timeperiod=20)

# Calculate the 50-day moving average
data['ma50'] = talib.SMA(data['close'], timeperiod=50)

# Calculate the Bollinger Bands
data['upper'], data['middle'], data['lower'] = talib.BBANDS(data['close'], timeperiod=20, nbdevup=2, nbdevdn=2)

# Define the entry and exit conditions for the strategy
data['long_entry'] = (data['close'] > data['upper']) & (data['close'].shift(1) <= data['upper'].shift(1))
data['long_exit'] = (data['close'] < data['ma20']) & (data['close'].shift(1) >= data['ma20'].shift(1))

# Define the initial capital and position size for the strategy
capital = 100000
position_size = 10  # Number of shares to trade

# Initialize the strategy variables
entry_price = 0
stop_loss = 0

# Monitor real-time price data using KiteConnect
while True:
    try:
        # Get the latest price data for the security
        ticker_data = kite.ltp(instrument_token)
        price = ticker_data[instrument_token]['last_price']
        
        # Check if the entry condition has been met
        if data['long_entry'][-1]:
            entry_price = price
            stop_loss = data['lower'][-1]
            quantity = int(capital * position_size / price)
            kite.place_order(variety=kite.VARIETY_REGULAR,
                             exchange=kite.EXCHANGE_NSE,
                             tradingsymbol='INFY',
                             transaction_type=kite.TRANSACTION_TYPE_BUY,
                             quantity=quantity,
                             order_type=kite.ORDER_TYPE_MARKET,
                             product=kite.PRODUCT_MIS)
            print(f'Long position taken at {entry_price}. Stop loss at {stop_loss}. Quantity: {quantity}')
            
        # Check if the exit condition has been met
        elif data['long_exit'][-1]:
            exit_price = price
            pnl = (exit_price - entry_price) * position_size
            capital += pnl
            print(f'Long position exited at {exit_price}. P&L: {pnl}. Capital: {capital}')
            entry_price = 0
            stop_loss = 0
            
        # Update the stop loss if necessary
        elif entry_price > 0 and price < stop_loss:
            exit_price = stop

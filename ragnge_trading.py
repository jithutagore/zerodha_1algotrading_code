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

# Define the securities to trade and the position size
securities = ['TATASTEEL', 'INFY', 'HDFCBANK']
position_size = 10  # Number of shares to trade

# Define the entry and exit conditions for the strategy
range_threshold = 1  # Minimum range percentage required for entry
range_direction = 'up'  # Range direction (up or down)
stop_loss = 0.5  # Stop loss percentage

# Define the initial capital for the strategy
capital = 100000

# Monitor real-time price data using KiteConnect
while True:
    try:
        # Get the latest price data for the securities
        ticker_data = kite.quote(securities)
        
        for security in securities:
            # Get the latest price and previous day's closing price for the security
            last_price = ticker_data[security]['last_price']
            prev_close = ticker_data[security]['ohlc']['close']
            
            # Calculate the range percentage
            if range_direction == 'up':
                high = ticker_data[security]['ohlc']['high']
                low = prev_close
            else:
                high = prev_close
                low = ticker_data[security]['ohlc']['low']
                
            range_pct = (high - low) / prev_close * 100
            
            # Check if the range condition has been met
            if range_pct > range_threshold and range_direction == 'up':
                entry_price = high
                stop_loss_price = entry_price * (1 - stop_loss / 100)
                quantity = int(capital * position_size / entry_price)
                kite.place_order(variety=kite.VARIETY_REGULAR,
                                 exchange=kite.EXCHANGE_NSE,
                                 tradingsymbol=security,
                                 transaction_type=kite.TRANSACTION_TYPE_BUY,
                                 quantity=quantity,
                                 order_type=kite.ORDER_TYPE_LIMIT,
                                 product=kite.PRODUCT_MIS,
                                 price=entry_price,
                                 trigger_price=entry_price)
                print(f'Long position taken in {security} at {entry_price}. Quantity: {quantity}')
                capital -= entry_price * quantity
            elif range_pct > range_threshold and range_direction == 'down':
                entry_price = low
                stop_loss_price = entry_price * (1 + stop_loss / 100)
                quantity = int(capital * position_size / entry_price)
                kite.place_order(variety=kite.VARIETY_REGULAR,
                                 exchange=kite.EXCHANGE_NSE,
                                 tradingsymbol=security,
                                 transaction_type=kite.TRANSACTION_TYPE_SELL,
                                 quantity=quantity,
                                 order_type=kite.ORDER_TYPE_LIMIT,
                                 product=kite.PRODUCT_MIS,
                                 price=entry_price,
                                 trigger_price=entry_price)
                print(f'Short position taken in {security} at {entry_price}. Quantity: {quantity}')
                capital += entry_price * quantity
                
        time.sleep(60)  # Wait for 1 minute before checking again
        
    except KiteException as e:
        print(e.message)



"""
This code defines the securities to trade and the position size at the top.
 The range_threshold variable specifies the minimum range percentage required for entry,
  and the `range

"""
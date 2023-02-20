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
gap_threshold = 0.5  # Minimum gap percentage required for entry
gap_direction = 'up'  # Gap direction (up or down)

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
            
            # Calculate the gap percentage
            if gap_direction == 'up':
                gap = (last_price - prev_close) / prev_close * 100
            else:
                gap = (prev_close - last_price) / prev_close * 100
            
            # Check if the gap condition has been met
            if gap > gap_threshold and gap_direction == 'up':
                quantity = int(capital * position_size / last_price)
                kite.place_order(variety=kite.VARIETY_REGULAR,
                                 exchange=kite.EXCHANGE_NSE,
                                 tradingsymbol=security,
                                 transaction_type=kite.TRANSACTION_TYPE_BUY,
                                 quantity=quantity,
                                 order_type=kite.ORDER_TYPE_MARKET,
                                 product=kite.PRODUCT_MIS)
                print(f'Long position taken in {security} at {last_price}. Quantity: {quantity}')
                capital -= last_price * quantity
            elif gap > gap_threshold and gap_direction == 'down':
                quantity = int(capital * position_size / last_price)
                kite.place_order(variety=kite.VARIETY_REGULAR,
                                 exchange=kite.EXCHANGE_NSE,
                                 tradingsymbol=security,
                                 transaction_type=kite.TRANSACTION_TYPE_SELL,
                                 quantity=quantity,
                                 order_type=kite.ORDER_TYPE_MARKET,
                                 product=kite.PRODUCT_MIS)
                print(f'Short position taken in {security} at {last_price}. Quantity: {quantity}')
                capital += last_price * quantity
                
        time.sleep(60)  # Wait for 1 minute before checking again
        
    except KiteException as e:
        print(e.message)

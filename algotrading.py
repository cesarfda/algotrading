import alpaca_trade_api as tradeapi
import numpy as np
import time
import os

'''
Creating connectiong with Alpaca API to retrieve market data and place orders
'''
KEY_ID = os.environ['PUB_KEY']
SEC_KEY = os.environ['SEC_KEY']
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= KEY_ID, secret_key=SEC_KEY, base_url=BASE_URL)

'''
Retrieve market data in the format of a numpy array of the last 15 minutes of price activity for a given ticker
'''
def get_data():
    market_data = api.get_barset(symb, 'minute', limit=15)
    
    close_list = []
    for bar in market_data[symb]:
        close_list.append(bar.c)
    
    close_list = np.array(close_list, dtype=np.float64)

    return close_list

'''
Place a buy order on alpaca for a given symbol and quantity
'''
def buy(q, s): # Returns nothing, makes call to buy stock
    api.submit_order(
        symbol=s,
        qty=q,
        side='buy',
        type='market',
        time_in_force='gtc'
    )

'''
Place a sell order on alpaca for a given symbol and quantity
'''
def sell(q, s): # Returns nothing, makes call to sell stock
    api.submit_order(
        symbol=s,
        qty=q,
        side='sell',
        type='market',
        time_in_force='gtc'
    )

'''
Determine what ticker will be used to trade
'''

symb = "SPY" # Ticker of stock you want to trade
pos_held = False

'''
Loop to execute the algortighm. The algorithm only executes if the market is open, otherwise it sleep for 30 minutes and checks
if the market is open again before trying to check prices or place orders
'''
while True:
    
    clock = api.get_clock()
    
    if clock.is_open:
      print("")
      print("Checking Price")
      
      close_list = get_data()

      ma = np.mean(close_list)
      last_price = close_list[-1]

      print("Moving Average: " + str(ma))
      print("Last Price: " + str(last_price))

      if ma + 0.1 < last_price and not pos_held:
          print("Buy")
          buy(25, symb)
          pos_held = True
      
      elif ma - 0.1 > last_price and pos_held:
          print("Sell")
          sell(25, symb)
          pos_held = False
      
      time.sleep(60)
    else:
      print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
      time.sleep(1800)    

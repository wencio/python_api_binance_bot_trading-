import requests
import matplotlib.pyplot as plt
import pandas as pd

from binance import Client
client = Client('API KEY', 'PRIVATE KEY')
print (client)

def getminutedata(symbol,interval,lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol,interval,lookback +'min ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time','Open','High','Low','Close','Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index,unit='ms')
    frame = frame.astype(float)
    return frame

test = getminutedata('BTCUSDT','1m','30')

print(test)
print(test.Open.plot())

#buy is the asset fell more than 0,2% within the last 30min
#sell if asset rises by more than 0.15% or fall futhers
#by 0.15% 

def strategytest(symbol,qty,entried=False):
    df = getminutedata(symbol,'1m','30m')
    cumulret = (df.Open.pct_change() +1).cumprod() -1
    if not entried:
        if cumulret [-1] < 0.002:
            order = client.create_order(symbol=symbol,side='BUY',type='MARKET',quantity=qty)
            print(order)
            entried = True
        else:
            print("No trade has been executed")
    if entried:
        while True:
            df = getminutedata(symbol,'1m','30m')
            sincebuy = df.loc[df.index > pd.to_datetime(order['transactTime'],unit='ms')]
            if len(sincebuy) > 0:
                sincebuyret = (sincebuy.Open.pct_change() +1).cumprod() -1
                if sincebuyret[-1] > 0.0015 or sincebuyret[-1] < -0.0015:
                    order = client.create_order(symbol=symbol,side='SELL',type='MARKET',quantity=qty)
                    print(order)
                    break
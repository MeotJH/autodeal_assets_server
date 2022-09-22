import pybithumb
import json

def bull_market_v1(ticker):
    df = pybithumb.get_ohlcv(ticker)
    ma5 = df['close'].rolling(window=5).mean()
    price = pybithumb.get_current_price(ticker)
    last_ma5 = ma5[-2]

    state = None
    if price > last_ma5:
        state = True
    else:
        state = False
    
    return json.dumps({ "price" : price, "last_ma5" : last_ma5, "state" : state})
    

